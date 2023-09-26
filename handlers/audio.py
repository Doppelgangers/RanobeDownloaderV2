import multiprocessing
from pathlib import Path
import re
import subprocess
import time
import settings


class Ffmpeg:
    """
    Для работы данного модуля в PATH должна быть утилита ffmpeg,
    в данном случае добавление происходит в settings или ввести полный путь до exe файла в : _ffmpeg
    """
    _ffmpeg = 'ffmpeg'

    def __init__(self, work_path: str, name_merge_file='merge.txt'):
        self.path = Path(work_path)
        self.path_merge_file = self.path.joinpath(name_merge_file)

    def _create_merge_file(self, file_paths: list[str]):
        with open(self.path_merge_file, 'w', encoding="utf-8") as file:
            file.writelines([f"""file '{path}'\n""" for path in file_paths])

    def _make_merge_in_files(self, filename: str = 'output.ts'):
        output_path = self.path.joinpath(filename)
        command = f"""{self._ffmpeg} -f concat -safe 0 -i "{self.path_merge_file}" -c copy "{output_path}"""
        subprocess.run(command, shell=True)

    def merge(self, paths_audio_files: list[str]):
        self._create_merge_file(paths_audio_files)
        self._make_merge_in_files()

    def convert_TS_to_MP3(self, path_ts, output, use_work_path: bool = True, del_old_file: bool = False):
        path_ts = self.path.joinpath(path_ts) if use_work_path else path_ts
        output = self.path.joinpath(output) if use_work_path else output
        del_command = f""" && del "{path_ts}" """
        command = f"""{self._ffmpeg} -i "{path_ts}" -vn -acodec libmp3lame "{output}" {del_command if del_command else ''}"""
        print(command)
        subprocess.run(command, shell=True)


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
        ls = [file_path.__str__() for file_path in path_aud.glob('seq*.ts')]
        return sorted(ls, key=lambda x: int(re.findall(r"seq(\d*).ts", x)[0]))


if __name__ == '__main__':
    map_pl = [{'name': '1 глава Неудавшаяся скульптура', 'offset': (0, 2211)}, {'name': '2 глава Сад богов', 'offset': (2211, 4739)}, {'name': '3 глава Выбор орков', 'offset': (4739, 6488)}, {'name': '4 глава Худшая судьба', 'offset': (6488, 8386)}, {'name': '5 глава Грабница короля Белсоса', 'offset': (8386, 10375)}, {'name': '6 глава Последний мастер Скульптуры', 'offset': (10375, 12187)}, {'name': '7 глава Скульптура короля духа', 'offset': (12187, 13872)}, {'name': '8 глава Выбор северных правителей', 'offset': (13872, 15717)}, {'name': '9 глава Деятельность оживленных скульптур', 'offset': (15717, 17586)}, {'name': '9.1 глава Ловушка племени саллионов', 'offset': (17586, -1)}]
    path_aud = Path(r'D:\dev\RanobeDownloaderV2\temp\Легендарный лунный скульптор. Том 29')

    pl = AudioSplitter(map_playlist=map_pl, path=path_aud.__str__())
    f = Ffmpeg(path_aud.__str__())
    # pl.create_merge_file()

    path_ts_list = pl.list_audio_files
    output_list = [i[:-2] + 'mp3' for i in path_ts_list]

    t = time.time()
    # pl.merge_files()
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    pool.starmap(f.convert_TS_to_MP3, zip(path_ts_list, output_list))
    pool.close()
    pool.join()
    # f.convert_TS_to_MP3(pl.list_audio_files[0], output_list[0])
    print(time.time()-t)



