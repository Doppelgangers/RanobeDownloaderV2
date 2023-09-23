import os
import pathlib
import settings
import pydub
from pydub import AudioSegment


class Splitter:

    def __init__(self, map_playlist: list[dict], path: pathlib.Path):
        self.map_playlist = map_playlist
        self.path = path

    @property
    def audio_map(self) -> zip:
        count_audios = list(path_aud.glob('*')).__len__()
        files_map = [f'seq{i}.ts' for i in range(count_audios)]
        duration_map = [29_977 if (dur + 1) % 128 == 0 else 30_000 for dur in range(count_audios)]
        return zip(files_map, duration_map)

    @property
    def split_list(self):
        res = []
        for item_playlist in self.map_playlist:

            return

    def find_point(self, value):
        buf = 0
        for filename, duration in self.audio_map:
            if buf > value:
                return (filename, abs(buf-value-duration))
            buf += duration

if __name__ == '__main__':
    map = [{'name': '1 глава Неудавшаяся скульптура', 'offset': (0, 2211)}, {'name': '2 глава Сад богов', 'offset': (2211, 4739)}, {'name': '3 глава Выбор орков', 'offset': (4739, 6488)}, {'name': '4 глава Худшая судьба', 'offset': (6488, 8386)}, {'name': '5 глава Грабница короля Белсоса', 'offset': (8386, 10375)}, {'name': '6 глава Последний мастер Скульптуры', 'offset': (10375, 12187)}, {'name': '7 глава Скульптура короля духа', 'offset': (12187, 13872)}, {'name': '8 глава Выбор северных правителей', 'offset': (13872, 15717)}, {'name': '9 глава Деятельность оживленных скульптур', 'offset': (15717, 17586)}, {'name': '9.1 глава Ловушка племени саллионов', 'offset': (17586, -1)}]
    path_aud = pathlib.Path(r'D:\dev\RanobeDownloaderV2\temp\Легендарный лунный скульптор. Том 29')


    splitter = Splitter(map, path_aud)
    audio_map = splitter.audio_map
    print(splitter.find_point(2211))
    # print(*spl.audio_map)
    # for p in range(0, 634):
    #     path = path_aud.joinpath(f'seq{p}.ts')
    #     # print(path)
    #     aud = AudioSegment.from_file(path.__str__(), ffmpeg=ffmpeg_path)
    #     if (len := aud.__len__()) != 30_000:
    #         print(len, p)



