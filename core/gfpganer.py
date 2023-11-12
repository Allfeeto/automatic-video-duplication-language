import os
import sys
import cv2
import torch
from basicsr.utils import img2tensor, tensor2img
from basicsr.utils.download_util import load_file_from_url
from facexlib.utils.face_restoration_helper import FaceRestoreHelper
from torchvision.transforms.functional import normalize

from gfpgan.archs.gfpgan_bilinear_arch import GFPGANBilinear
from gfpgan.archs.gfpganv1_arch import GFPGANv1
from gfpgan.archs.gfpganv1_clean_arch import GFPGANv1Clean


class GFPGANer():
    """Помощник для восстановления с помощью GFPGAN.

 Он обнаружит и обрежет грани, а затем изменит размер граней до 512x512.
 GFPGAN используется для восстановления граней с измененным размером.
 Фон повышается с помощью bg_upsampler.
 Наконец, лица будут вставлены обратно в фоновое изображение с увеличенной выборкой.

 Аргументы:
 model_path (str): Путь к модели GFPGAN. Это могут быть URL-адреса (сначала они будут загружены автоматически).
 upscale (float): увеличение масштаба конечного результата. По умолчанию: 2.
arch (str): Архитектура GFPGAN. Параметр: чистый | оригинальный. По умолчанию: чистый.
 channel_multiplier (int): Множитель каналов для больших сетей StyleGAN2. По умолчанию: 2.
 bg_upsampler (nn.Module): Повышающий выборку для фона. По умолчанию: Нет.
    """

    def __init__(self, model_path, root_dir, upscale=2, arch='clean', channel_multiplier=2, bg_upsampler=None, device=None):
        self.upscale = upscale
        self.bg_upsampler = bg_upsampler

        # инициализировать модель
        self.device = device
        # инициализируйте GFP-GAN
        if arch == 'clean':
            self.gfpgan = GFPGANv1Clean(
                out_size=512,
                num_style_feat=512,
                channel_multiplier=channel_multiplier,
                decoder_load_path=None,
                fix_decoder=False,
                num_mlp=8,
                input_is_latent=True,
                different_w=True,
                narrow=1,
                sft_half=True)
        elif arch == 'bilinear':
            self.gfpgan = GFPGANBilinear(
                out_size=512,
                num_style_feat=512,
                channel_multiplier=channel_multiplier,
                decoder_load_path=None,
                fix_decoder=False,
                num_mlp=8,
                input_is_latent=True,
                different_w=True,
                narrow=1,
                sft_half=True)
        elif arch == 'original':
            self.gfpgan = GFPGANv1(
                out_size=512,
                num_style_feat=512,
                channel_multiplier=channel_multiplier,
                decoder_load_path=None,
                fix_decoder=True,
                num_mlp=8,
                input_is_latent=True,
                different_w=True,
                narrow=1,
                sft_half=True)
        elif arch == 'RestoreFormer':
            from gfpgan.archs.restoreformer_arch import RestoreFormer
            self.gfpgan = RestoreFormer()
        # инициализировать face helper
        self.face_helper = FaceRestoreHelper(
            upscale,
            face_size=512,
            crop_ratio=(1, 1),
            det_model='retinaface_resnet50',
            save_ext='png',
            use_parse=True,
            device=self.device,
            model_rootpath=root_dir)

        if model_path.startswith('https://'):
            model_path = load_file_from_url(
                url=model_path, model_dir=root_dir, progress=True, file_name=None)
            # Установите разрешение для Windows на доступ к файлам fpga
            if sys.platform == 'win32':
                try:
                    cmd = f'icacls "{model_path}" /grant:r "Users:(R,W)" /T'
                    os.system(cmd)
                except Exception as e:
                    print(e)
        loadnet = torch.load(model_path)
        if 'params_ema' in loadnet:
            keyname = 'params_ema'
        else:
            keyname = 'params'
        self.gfpgan.load_state_dict(loadnet[keyname], strict=True)
        self.gfpgan.eval()
        self.gfpgan = self.gfpgan.to(self.device)

    @torch.no_grad()
    def enhance(self, img, has_aligned=False, only_center_face=False, paste_back=True, weight=0.5):
        self.face_helper.clean_all()

        if has_aligned:  # входные данные уже выровнены
            img = cv2.resize(img, (512, 512))
            self.face_helper.cropped_faces = [img]
        else:
            self.face_helper.read_image(img)
            # получите ориентиры для каждого лица
            self.face_helper.get_face_landmarks_5(
                only_center_face=only_center_face, eye_dist_threshold=5)
            # выровняйте и деформируйте каждую грань
            self.face_helper.align_warp_face()

        # восстановление лица
        for cropped_face in self.face_helper.cropped_faces:
            # подготовка данных
            cropped_face_t = img2tensor(
                cropped_face / 255., bgr2rgb=True, float32=True)
            normalize(cropped_face_t, (0.5, 0.5, 0.5),
                      (0.5, 0.5, 0.5), inplace=True)
            cropped_face_t = cropped_face_t.unsqueeze(0).to(self.device)

            try:
                output = self.gfpgan(
                    cropped_face_t, return_rgb=False, weight=weight)[0]
                # преобразовать в изображение
                restored_face = tensor2img(output.squeeze(
                    0), rgb2bgr=True, min_max=(-1, 1))
            except RuntimeError as error:
                print(f'\tFailed inference for GFPGAN: {error}.')
                restored_face = cropped_face

            restored_face = restored_face.astype('uint8')
            self.face_helper.add_restored_face(restored_face)

        if not has_aligned and paste_back:
            # увеличьте выборку фона
            if self.bg_upsampler is not None:
                # Теперь поддерживается только RealESRGAN для повышения фоновой дискретизации
                bg_img = self.bg_upsampler.enhance(
                    img, outscale=self.upscale)[0]
            else:
                bg_img = None

            self.face_helper.get_inverse_affine(None)
            # вставьте каждое восстановленное лицо во входное изображение
            restored_img = self.face_helper.paste_faces_to_input_image(
                upsample_img=bg_img)
            return self.face_helper.cropped_faces, self.face_helper.restored_faces, restored_img
        else:
            return self.face_helper.cropped_faces, self.face_helper.restored_faces, None
