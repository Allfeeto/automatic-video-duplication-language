
<h1 align="center">Установка</h1>


  <li>Клонируйте это репозиторий</li>

  <li>Установите <a href = 'https://conda.io/projects/conda/en/latest/user-guide/install/'>conda</a> </li>

  <li>Создайте среду с помощью Python 3.10</li>

  <li>Активировать среду</li><br>
  
      conda create --name your_name python=3.10

Требования к установке:

    python install.py
<br><br>

  <li>В файле config.json измените аргумент HF_TOKEN. Это ваш токен HuggingFace. </li>

  <li>Посетите спикера- <a href = 'https://huggingface.co/pyannote/segmentation'>ведение дневника, сегментация</a> и примите условия пользователя.  - <a href='https://huggingface.co/settings/tokens'>здесь</a> создайте токен (write)</li>

  <li>Загрузите веса с <a href='https://drive.google.com/file/d/1dYy24q_67TmVuv_PbChe2t1zpNYJci1J/view'>диска</a>, распакуйте загруженный файл в папку <b>weights</b></li>

  <li>Установите <a href='https://ffmpeg.org/'>ffmpeg</a><br><br>


<>bКонфигурации (config.json)</b>

|Значние | Описание|
|-|-|
| DET_TRESH |	Технология распознавания лиц [0.0: 1.0] |
|DIST_TRESH |	Расстояние встраивания граней ограничено [0.0: 1.0] |
| HF_TOKEN	| Ваш токен HuggingFace|
| USE_ENHANCER |	Нужно ли нам улучшать лица с помощью GFPGAN?<br> |


<h3>Поддерживаемые языки</h3>

Албанский, амхарский, арабский, Армянский, азербайджанский, баскский, бенгальский, болгарский, каталанский, кебуано, чичева, Китайский, голландский, Английский, Финский, французский, Немецкий, греческий, гуджарати, гаитянский креольский, хауса, иврит, хинди, Венгерский, Исландский, Индонезийский, яванский, каннада, казахский, кхмерский, корейский, Киргизский, лаосский, Латинский, латышский, малагасийский, малайский, малаялам, маратхи , Монгольский, одиа, Персидский, Польский, Португальский, панджаби, Румынский, Русский, Самоанский, шона, Сомалийский, Испанский, суахили, Шведский, Таджикский, Тамильский, телугу, Тайский, Турецкий, Украинский, Вьетнамский, валлийский, йоруба

языки прописаны [здесь](rutubetrans/core/mapper.py)





<h1 align="center">Использование</h1>

  <li>Активируйте свою среду:</li><br>

      conda activate your_name  
  
  <li>Путь от компакт-диска к проекту:</li><br>

      cd path_to_project
  <br>

В корне проекта есть скрипт перевода, который переводит установленное вами видео.

  <li>video_filename - имя файла вашего входного видео (.mp4)</li>

  <li>output_language - язык, на который будет выполнен перевод. Предоставляется здесь (вы также можете найти его в коде (маппер))</li>

  <li>output_filename - имя файла выходного видео (.mp4)</li><br>

    python translate.py video_filename output_language -o output_filename


также есть скрипт для наложения голоса на видео с синхронизацией губ, который позволяет создавать видео с человеком, произносящим вашу речь. В настоящее время это работает для видео с одним человеком.

  <li>voice_filename - имя файла вашей речи (.wav)</li>

  <li>video_filename - имя файла вашего входного видео (.mp4)</li>

  <li>output_filename - имя файла выходного видео (.mp4)</li><br>

    python speech_changer.py voice_filename video_filename -o output_filename 
<br><br>


<h2>Как это работает</h2>

1. Обнаружение сцен ([PySceneDetect](https://github.com/Breakthrough/PySceneDetect))

2. Распознавание лиц [yolov8-face](https://github.com/akanametov/yolov8-face)

3. Повторная идентификация [deepface](https://github.com/serengil/deepface)

4. Улучшение речи [MDXNet](https://huggingface.co/freyza/kopirekcover/blob/main/MDXNet.py)

5. Транскрипция и ведение дневника говорящих [whisperX](https://github.com/m-bain/whisperX)

6. Перевод текста [googletrans](https://pypi.org/project/googletrans/)

7. Клонирование голоса [TTS](https://github.com/coqui-ai/TTS)

8. Синхронизация губ [lipsync](https://github.com/mowshon/lipsync)

9. Восстановление лица [GFPGAN](https://github.com/TencentARC/GFPGAN)




