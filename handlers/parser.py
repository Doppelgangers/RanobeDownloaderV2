import re

import requests
from bs4 import BeautifulSoup
import m3u8


class Parser:

    def __init__(self, html_code):
        self.soup = BeautifulSoup(html_code, "lxml")

    @staticmethod
    def get_html_for_file(filename):
        html_code = ""
        with open(filename, 'r', encoding="utf-8") as f:
            html_list = f.readlines()
        for line in html_list:
            html_code += line
        return html_code


class ParserM3U8:
    def __init__(self, url=''):
        self.url = url
        self.playlist = m3u8.load(url)
        self.id = self._get_id()

    @property
    def key(self):
        for keys in self.playlist.keys:
            key = requests.get(keys.uri).content
            return key

    @property
    def iv(self):
        for keys in self.playlist.keys:
            return bytes.fromhex(keys.iv[2::])

    def _get_id(self):
        return re.findall(r'b.(\d*).pl', self.url)[0]

    @property
    def base_url(self):
        return self.playlist.base_uri

    def get_list_ts_link(self):
        return [seq.absolute_uri for seq in self.playlist.segments]


class ParserAkniga(Parser):

    def __init__(self, html_code):
        super().__init__(html_code)

    @property
    def title(self) -> str:
        return self.soup.find('div', class_='caption__article-title').text.strip()

    @property
    def audio_map(self) -> list:
        """Получает список словарей с названием главы и отступами """
        """ [ {'name' : "Name 1" , 'offset' : 0 } ... ]"""
        data = []

        item = self.soup.findAll(class_="chapter__default")
        name = self.soup.findAll(class_="chapter__default--title")
        item.pop(0)
        name.pop(0)

        for i in range(len(item)):
            try:
                data.append(
                    {
                        "name": name[i].text,
                        "offset": (int(item[i]['data-pos']), int(item[i+1]['data-pos']))
                    }
                )
            except IndexError:
                data.append(
                    {
                        "name": name[i].text,
                        "offset": (int(item[i]['data-pos']), -1)
                    }
                )

        return data

    @property
    def reader(self):
        return data.text.strip() if (data := self.soup.find(class_="link__reader")) else ""

    @property
    def series(self):
        return data.text.strip() if (data := self.soup.find(class_="link__series")) else ""

    @property
    def author(self):
        return data.text.strip() if (data := self.soup.find(class_="link__author")) else ""

