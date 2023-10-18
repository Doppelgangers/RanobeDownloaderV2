import pathlib
import time
import logging

import settings
from handlers import AKnigaWebPage, ParserM3U8, CryptoDownloader, ParserAkniga, AudioSplitter


def main():
    print(r"""
     ______    ___    _   _   _____  ______   _____   
     | ___ \  / _ \  | \ | | |  _  | | ___ \ |  ___|  
     | |_/ / / /_\ \ |  \| | | | | | | |_/ / | |__    
     |    /  |  _  | | . ` | | | | | | ___ \ |  __|   .    . .__.
     | |\ \  | | | | | |\  | \ \_/ / | |_/ / | |___    \  /  .__|
     \_| \_| \_| |_/ \_| \_/  \___/  \____/  \____/     \/   |__.
    """)
    url = input("Write url: ")
    # url = r'https://akniga.org/nam-hi-sunga-legendarnyy-lunnyy-skulptor-tom-29'

    page_akniga = AKnigaWebPage(url)
    logging.info("Парсинг сайта")
    t = time.time()

    logging.info(f"Парсинг сайта завершён за {time.time() - t}")

    m3u8 = ParserM3U8(page_akniga.m3u8_link)
    page_akniga = ParserAkniga(html_code=page_akniga.html_code)
    path_download = pathlib.Path(settings.ROOT_PATH, 'temp', page_akniga.title)

    downloader = CryptoDownloader(key=m3u8.key, iv=m3u8.iv, path=path_download)
    logging.info("Загрузка исходников")
    t = time.time()
    downloader.async_download(m3u8.get_list_ts_link())
    logging.info(f"Исходники скачались за {time.time() - t} секунды ")

    audio = AudioSplitter(map_playlist=page_akniga.audio_map, path=path_download)
    logging.info("Начало конвертации загруженный аудиофайлов")
    t = time.time()
    audio.convert_ts_to_mp3(ts_paths=audio.list_seq_ts_files)
    logging.info(f"Файлы конвертировались за {time.time() - t}")

    logging.info("Объеденение аудиофайлов")
    t = time.time()
    audio.merge()
    logging.info(f"Файлы объеденились за {time.time() - t}")

    audio.del_templates()
    logging.info("Шаблоны удалены")

    logging.info("Нарезка аудиофайлов")
    t = time.time()
    audio.slice(path_save_folder=settings.SAVE_PATH.joinpath(page_akniga.title), artist=page_akniga.author, album=page_akniga.title)
    logging.info(f"Файлы нарезались за  {time.time() - t}")

    logging.info("Удаление мусора")
    audio.del_temp_folder()

    print(rf"""
     _____   _   _  ______ 
    |  ___| | \ | | |  _  \
    | |__   |  \| | | | | |
    |  __|  | . ` | | | | |
    | |___  | |\  | | |/ / 
    \____/  \_| \_/ |___/  
    
    Загруженные файлы хранятся в {settings.SAVE_PATH.joinpath(page_akniga.title)}
    """)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()


