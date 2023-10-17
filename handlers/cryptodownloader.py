import pathlib
import aiohttp
import aiofiles
import asyncio
from Crypto.Cipher import AES


class CryptoDownloader:

    def __init__(self, key: bytes, iv: bytes, path: pathlib.Path = pathlib.Path('temp')):
        self.cipher = AES.new(key, AES.MODE_CBC, iv)
        if not path.exists():
            path.mkdir(parents=True)
        self.path = path

    def async_download(self, urls, ):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._async_create_download_map(urls))

    async def _async_create_download_map(self, url_list):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for url in url_list:
                task = asyncio.create_task(self._async_download_file(session, url))
                tasks.append(task)
            await asyncio.gather(*tasks)

    async def _async_download_file(self, session, url: str):
        async with session.get(url) as response:
            if response.status == 200:
                filename = url.split('/')[-1]
                async with aiofiles.open(pathlib.Path(self.path, filename), "wb") as file:
                    while True:
                        chunk = await response.content.read()
                        if len(chunk) == 0:
                            break
                        await file.write(self.cipher.decrypt(chunk))
            else:
                print(f"Не удалось загрузить файл {url}. Код состояния: {response.status}")

