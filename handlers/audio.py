import os
import pathlib
import re

import settings
import pydub
from pydub import AudioSegment


class AudioPoint:
    _ms = 0

    def __init__(self, file_name, time_milliseconds=0, time_seconds=0):
        self.file_name = file_name

        if time_seconds: self.time_seconds = time_seconds
        else: self.time_milliseconds = time_milliseconds

    def __str__(self):
        return f"{self.__class__.__name__}({self.file_name}, {self.time_seconds})"

    def __int__(self):
        return self.file_id

    @property
    def file_id(self) -> int:
        return int(re.findall(r'seq(\d*)', self.file_name)[0])

    @property
    def time_seconds(self):
        return self._ms / 1000

    @time_seconds.setter
    def time_seconds(self, value):
        self._ms = value * 1000

    @property
    def time_milliseconds(self):
        return self._ms

    @time_milliseconds.setter
    def time_milliseconds(self, value):
        self._ms = value


class Playlist:

    def __init__(self, map_playlist: list[dict], path: str):
        """
        Создаёт абстрактный плейлист для взаимодействия с ним

        :param map_playlist: Структура плейлиста [{"name": 'название композиции', offset: (0, 600)}, ...]
        p.s: offset обозначает фрагмент аудиофайла относительно общего аудиофайла
        в формате (начало фрагмента в секундах, конец фрагмента)

        :param path: путь к фрагментам плейлиста из файлов 'seq{number}.ts'
        """
        self.map_playlist = map_playlist
        self.path = path

    def __len__(self) -> int:
        return self.map_playlist.__len__()

    @property
    def count_audios(self) -> int:
        return list(path_aud.glob('*')).__len__()

    def find_point(self, value) -> AudioPoint:
        file_name = f"seq{value // 30}.ts"
        time_seconds = value % 30
        if value == -1:
            file_name = f'seq{self.count_audios - 1}.ts'
            time_seconds = -1
        return AudioPoint(file_name=file_name, time_seconds=time_seconds)

    def find_slice(self, start_point: int, end_point: int):
        start_point = self.find_point(start_point)
        end_point = self.find_point(end_point)
        print(start_point, end_point)

        if start_point.time_seconds == 0:
            print(f"{start_point.file_name} C начала")
        if (count := end_point.file_id - start_point.file_id) > 0:
            print(count)

            list_download = [i for i in range(start_point.file_id, end_point.file_id)]
            print(list_download)

        if end_point.time_seconds == 0:
            print(f'seq{end_point.file_id-1}.ts Полностью')
        if end_point.time_seconds < 0:
            print('До конца')


if __name__ == '__main__':
    map = [{'name': '1 глава Неудавшаяся скульптура', 'offset': (0, 2211)}, {'name': '2 глава Сад богов', 'offset': (2211, 4739)}, {'name': '3 глава Выбор орков', 'offset': (4739, 6488)}, {'name': '4 глава Худшая судьба', 'offset': (6488, 8386)}, {'name': '5 глава Грабница короля Белсоса', 'offset': (8386, 10375)}, {'name': '6 глава Последний мастер Скульптуры', 'offset': (10375, 12187)}, {'name': '7 глава Скульптура короля духа', 'offset': (12187, 13872)}, {'name': '8 глава Выбор северных правителей', 'offset': (13872, 15717)}, {'name': '9 глава Деятельность оживленных скульптур', 'offset': (15717, 17586)}, {'name': '9.1 глава Ловушка племени саллионов', 'offset': (17586, -1)}]
    path_aud = pathlib.Path(r'D:\dev\RanobeDownloaderV2\temp\Легендарный лунный скульптор. Том 29')

    pl = Playlist(map_playlist=map, path=path_aud.__str__())
    # print(pl.count_audios)
    # audio_map = pl.audio_map
    slice = pl.find_slice(1, 2)
    # print(slice)
    # print(*spl.audio_map)
    # for p in range(0, 634):
    #     path = path_aud.joinpath(f'seq{p}.ts')
    #     # print(path)
    #     aud = AudioSegment.from_file(path.__str__(), ffmpeg=ffmpeg_path)
    #     if (len := aud.__len__()) != 30_000:
    #         print(len, p)



