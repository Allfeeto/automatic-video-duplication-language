
<h1 align="center">Установка</h1>

<li>Клонируйте это репозиторий</li>

<li>Установите [conda](https://conda.io/projects/conda/en/latest/user-guide/install/)</li>

<li>Создайте среду с помощью Python 3.10</li>

<li>Активировать среду</li>

Требования к установке:

python install.py


В файле config.json измените аргумент HF_TOKEN. Это ваш токен HuggingFace. Посетите спикера-ведение дневника, сегментация (https://huggingface.co/pyannote/segmentation) и примите условия пользователя. https://huggingface.co/settings/tokens - здесь создайте токен (write)
Загрузите веса с диска (https://drive.google.com/file/d/1dYy24q_67TmVuv_PbChe2t1zpNYJci1J/view), распакуйте загруженный файл в папку weights
Установите ffmpeg (https://ffmpeg.org/)

Конфигурации (config.json)
DET_TRESH	Технология распознавания лиц [0.0: 1.0]
DIST_TRESH	Расстояние встраивания граней ограничено [0.0: 1.0]
HF_TOKEN	Ваш токен HuggingFace
USE_ENHANCER	Нужно ли нам улучшать лица с помощью GFPGAN?

Поддерживаемые языки

Албанский, амхарский, арабский, Армянский, азербайджанский, баскский, бенгальский, болгарский, каталанский, кебуано, чичева, Китайский, голландский, Английский, Финский, французский, Немецкий, греческий, гуджарати, гаитянский креольский, хауса, иврит, хинди, Венгерский, Исландский, Индонезийский, яванский, каннада, казахский, кхмерский, корейский, Киргизский, лаосский, Латинский, латышский, малагасийский, малайский, малаялам, маратхи , Монгольский, одиа, Персидский, Польский, Португальский, панджаби, Румынский, Русский, Самоанский, шона, Сомалийский, Испанский, суахили, Шведский, Таджикский, Тамильский, телугу, Тайский, Турецкий, Украинский, Вьетнамский, валлийский, йоруба

<h1 align="center">Использование</h1>
Активируйте свою среду:
  conda activate your_env_name
Путь от компакт-диска к проекту:
  cd path_to_project

В корне проекта есть скрипт перевода, который переводит установленное вами видео.

video_filename - имя файла вашего входного видео (.mp4)
output_language - язык, на который будет выполнен перевод. Предоставляется здесь (вы также можете найти его в коде (маппер))
output_filename - имя файла выходного видео (.mp4)

python translate.py video_filename output_language -o output_filename


также есть скрипт для наложения голоса на видео с синхронизацией губ, который позволяет создавать видео с человеком, произносящим вашу речь. В настоящее время это работает для видео с одним человеком.

voice_filename - имя файла вашей речи (.wav)
video_filename - имя файла вашего входного видео (.mp4)
output_filename - имя файла выходного видео (.mp4)

python speech_changer.py voice_filename video_filename -o output_filename


Как это работает

Обнаружение сцен (PySceneDetect)https://github.com/Breakthrough/PySceneDetect
Распознавание лиц (yolov8-face)https://github.com/akanametov/yolov8-face
Повторная идентификация (deepface)https://github.com/serengil/deepface
Улучшение речи (MDXNet)https://huggingface.co/freyza/kopirekcover/blob/main/MDXNet.py
Транскрипция и ведение дневника говорящих (whisperX)https://github.com/m-bain/whisperX
Перевод текста (googletrans)https://pypi.org/project/googletrans/
Клонирование голоса (TTS)https://github.com/coqui-ai/TTS
Синхронизация губ (lipsync)https://github.com/mowshon/lipsync
Восстановление лица (GFPGAN)https://github.com/TencentARC/GFPGAN




