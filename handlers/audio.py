import os
import pathlib
import re
import subprocess

import settings
import pydub
from pydub import AudioSegment


class AudioSplitter:

    def __init__(self, map_playlist: list[dict], path: str):
        """

        :param map_playlist: Структура плейлиста [{"name": 'название композиции', offset: (0, 600)}, ...]
        p.s: offset обозначает фрагмент аудиофайла относительно общего аудиофайла
        в формате (начало фрагмента в секундах, конец фрагмента)

        :param path: путь к фрагментам плейлиста из файлов 'seq{number}.ts'
        """
        self.map_playlist = map_playlist
        self.path = path

    @property
    def list_audio_files(self) -> list:
        ls = [file_path.__str__() for file_path in path_aud.glob('*.ts')]
        return sorted(ls, key=lambda x: int(re.findall(r"seq(\d*).ts", x)[0]))

    def create_merge_file(self):
        with open(pathlib.Path(self.path, 'merge.txt'), 'w') as file:
            file.writelines([f"file '{ts_path}'\n" for ts_path in self.list_audio_files])


    def merge_files(self):
        command = f"""ffmpeg -f concat -safe 0 -i {pathlib.Path(self.path, 'merge.txt')} -c copy output.ts && rm seq*.ts"""
        # print(command)
        subprocess.run(command, shell=True)

if __name__ == '__main__':
    map = [{'name': '1 глава Неудавшаяся скульптура', 'offset': (0, 2211)}, {'name': '2 глава Сад богов', 'offset': (2211, 4739)}, {'name': '3 глава Выбор орков', 'offset': (4739, 6488)}, {'name': '4 глава Худшая судьба', 'offset': (6488, 8386)}, {'name': '5 глава Грабница короля Белсоса', 'offset': (8386, 10375)}, {'name': '6 глава Последний мастер Скульптуры', 'offset': (10375, 12187)}, {'name': '7 глава Скульптура короля духа', 'offset': (12187, 13872)}, {'name': '8 глава Выбор северных правителей', 'offset': (13872, 15717)}, {'name': '9 глава Деятельность оживленных скульптур', 'offset': (15717, 17586)}, {'name': '9.1 глава Ловушка племени саллионов', 'offset': (17586, -1)}]
    path_aud = pathlib.Path(r'D:\dev\RanobeDownloaderV2\temp\Легендарный лунный скульптор. Том 29')

    pl = AudioSplitter(map_playlist=map, path=path_aud.__str__())
    pl.merge_files()
    # print()
    # print(pl.list_audio_files)


