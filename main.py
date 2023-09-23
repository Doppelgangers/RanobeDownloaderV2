import pathlib
import time
import logging

from handlers import SiteChecker, ParserM3U8, CryptoDownloader, ParserAkniga


def main():
    print(r"""
     ______    ___    _   _   _____  ______   _____   
     | ___ \  / _ \  | \ | | |  _  | | ___ \ |  ___|  
     | |_/ / / /_\ \ |  \| | | | | | | |_/ / | |__    
     |    /  |  _  | | . ` | | | | | | ___ \ |  __|   .    . .__.
     | |\ \  | | | | | |\  | \ \_/ / | |_/ / | |___    \  /  .__|
     \_| \_| \_| |_/ \_| \_/  \___/  \____/  \____/     \/   |__.
    """)
    # url = input("Write url: ")
    url = r'https://akniga.org/nam-hi-sunga-legendarnyy-lunnyy-skulptor-tom-29'

    browser = SiteChecker()
    logging.info("Парсинг сайта")
    t = time.time()
    m3u8, html = browser.get_akniga_page(url).values()
    logging.info(f"Парсинг сайта завершён за {time.time() - t}")

    m3u8 = ParserM3U8(m3u8)
    page_akniga = ParserAkniga(html_code=html)
    path_download = pathlib.Path('temp', page_akniga.title)
    print(page_akniga.audio_map)

    downloader = CryptoDownloader(key=m3u8.key, iv=m3u8.iv, path=path_download)
    logging.info("Начало загрузки исходников")
    # t = time.time()
    # # downloader.async_download(m3u8.get_list_ts_link())
    # # logging.info(f"Исходники скачались за {time.time() - t} секунды ")
    # # print(f"Исходники лежат по пути: ", pathlib.Path.cwd().joinpath(path_download))

    print(r"""
     _____   _   _  ______ 
    |  ___| | \ | | |  _  \
    | |__   |  \| | | | | |
    |  __|  | . ` | | | | |
    | |___  | |\  | | |/ / 
    \____/  \_| \_/ |___/  
    """)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()






