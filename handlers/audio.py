import datetime
import logging
import multiprocessing
from pathlib import Path
import re
import subprocess
import time
import settings


class CommandLine:
    @staticmethod
    def execute(command):
        if settings.DEBUG:
            print(command)
            subprocess.run(command, shell=True)
            return
        subprocess.run(command, shell=True, stderr=subprocess.DEVNULL)


class Ffmpeg:
    """
    Для работы данного модуля в PATH должна быть утилита ffmpeg_mini,
    в данном случае добавление происходит в settings или ввести полный путь до exe файла в : _ffmpeg
    """

    def __init__(self, work_path: str | Path, name_merge_file='merge.txt', path_ffmpeg: str | Path = None):
        self.path = Path(work_path)
        self.path_merge_file = self.path.joinpath(name_merge_file)
        self._ffmpeg = path_ffmpeg if path_ffmpeg else 'ffmpeg'

    def _create_merge_file(self, file_paths: list[str]):
        with open(self.path_merge_file, 'w', encoding="utf-8") as file:
            file.writelines([f"""file '{path}'\n""" for path in file_paths])

    def _make_merge_in_files(self, filename: str = 'output.ts'):
        output_path = self.path.joinpath(filename)
        command = f"""{self._ffmpeg} -f concat -safe 0 -i "{self.path_merge_file}" -c copy "{output_path}"""
        CommandLine.execute(command)

    def del_merge_file(self):
        command = f"""del "{self.path_merge_file}" """
        CommandLine.execute(command)

    def merge(self, paths_audio_files: list[str], output: str = 'output.mp3', use_base_path: bool = True):
        self._create_merge_file(paths_audio_files)
        path = self.path.joinpath(output) if use_base_path else output
        self._make_merge_in_files(path)

    def convert_TS_to_MP3(self, path_ts, output, del_old_file: bool = False, use_work_path: bool = True,):
        path_ts = self.path.joinpath(path_ts) if use_work_path else path_ts
        output = self.path.joinpath(output) if use_work_path else output
        del_command = f"""del "{path_ts}" """
        command = f"""{self._ffmpeg} -i "{path_ts}" -vn -acodec libmp3lame "{output}" {' && ' + del_command if del_old_file else ''}"""
        CommandLine.execute(command)

    def split_audio(self, input_file, output_file, start_time: int, end_time: int, metadata=None):
        """

        :param input_file: путь к входящему файлу
        :param output_file: путь в выходящему файлу
        :param start_time: время начало отреза в секундах
        :param end_time: время конца отреза в секундах
        :param metadata: список метатегов типа ['-metadata', 'album=Название альбома'
        :return:
        """
        if metadata is None:
            metadata = []

        command = [self._ffmpeg]
        cmd_input = [f'-i', input_file]
        cmd_start_time = ['-ss', str(datetime.timedelta(seconds=start_time))]
        cmd_end_time = ['-to', str(datetime.timedelta(seconds=end_time))]
        cmd_codec = ['-c', 'copy']
        cmd_output = [output_file]
        command += cmd_input + cmd_start_time + (cmd_end_time if end_time != -1 else []) + cmd_codec + metadata + cmd_output
        print(command)
        CommandLine.execute(command)


class AudioSplitter:

    def __init__(self, map_playlist: list[dict], path: str | Path):
        """
        :param map_playlist: Структура плейлиста [{"name": 'название композиции', offset: (0, 600)}, ...]
        p.s: offset обозначает фрагмент аудиофайла относительно общего аудиофайла
        в формате (начало фрагмента в секундах, конец фрагмента)

        :param path: путь к фрагментам плейлиста из файлов 'seq{number}.ts'
        """
        self.map_playlist = map_playlist
        self.path = Path(path)

    @property
    def list_seq_ts_files(self) ->  list[str | Path]:
        ls = [file_path.__str__() for file_path in path_aud.glob('seq*.ts')]
        return sorted(ls, key=lambda x: int(re.findall(r"seq(\d*).ts", x)[0]))

    @property
    def list_seq_mp3_files(self) -> list[str | Path]:
        ls = [file_path.__str__() for file_path in path_aud.glob('seq*.mp3')]
        return sorted(ls, key=lambda x: int(re.findall(r"seq(\d*).mp3", x)[0]))

    def del_templates(self):
        command = f"""del "{self.path.joinpath('seq*')}" """
        CommandLine.execute(command)

    def convert_ts_to_mp3(self, ts_paths: list[str | Path], new_mp3_paths:  list[str | Path] = None, del_old_file: bool = True):
        ffmpeg = Ffmpeg(self.path)
        output_list = [i[:-2] + 'mp3' for i in ts_paths] if new_mp3_paths is None else new_mp3_paths

        pool = multiprocessing.Pool(processes=multiprocessing.cpu_count()*2)
        pool.starmap(ffmpeg.convert_TS_to_MP3, zip(ts_paths, output_list, [del_old_file]*ts_paths.__len__()))
        pool.close()
        pool.join()

    def merge(self):
        ffmpeg = Ffmpeg(self.path)
        ffmpeg.merge(self.list_seq_mp3_files)
        ffmpeg.del_merge_file()
        self.del_templates()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    map_pl = [{'name': '1 глава Неудавшаяся скульптура', 'offset': (0, 2211)}, {'name': '2 глава Сад богов', 'offset': (2211, 4739)}, {'name': '3 глава Выбор орков', 'offset': (4739, 6488)}, {'name': '4 глава Худшая судьба', 'offset': (6488, 8386)}, {'name': '5 глава Грабница короля Белсоса', 'offset': (8386, 10375)}, {'name': '6 глава Последний мастер Скульптуры', 'offset': (10375, 12187)}, {'name': '7 глава Скульптура короля духа', 'offset': (12187, 13872)}, {'name': '8 глава Выбор северных правителей', 'offset': (13872, 15717)}, {'name': '9 глава Деятельность оживленных скульптур', 'offset': (15717, 17586)}, {'name': '9.1 глава Ловушка племени саллионов', 'offset': (17586, -1)}]
    path_aud = Path(r'D:\dev\RanobeDownloaderV2\temp\Легендарный лунный скульптор. Том 29')

    pl = AudioSplitter(map_playlist=map_pl, path=path_aud.__str__())

    # logging.debug("Начало конвертации загруженный аудиофайлов")
    # t = time.time()
    # pl.convert_ts_to_mp3(ts_paths=pl.list_seq_ts_files)

    # logging.debug(f"Файлы конвертировались за {time.time()-t}")

    logging.debug("Начало объеденения аудиофайлов")
    t = time.time()
    # pl.del_templates()

    # command = [
    #     'ffmpeg',
    #     f'-i',
    #     path_aud.joinpath("output.mp3"),
    #
    #     '-ss',
    #     str(datetime.timedelta(seconds=30)),
    #
    #     '-to',
    #     str(datetime.timedelta(seconds=90)),
    #
    #     '-c',
    #     'copy',
    #
    #     path_aud.joinpath("2.mp3"),
    # ]
    # CommandLine.execute(command)
    f = Ffmpeg(path_aud)
    f.split_audio(path_aud.joinpath("output.mp3"), path_aud.joinpath("9.mp3"), 17586, -1 , ['-metadata', 'album=GGG'] )

    # print(path_aud.joinpath("1.mp3)"))
    # pl.merge()
    logging.debug(f"Файлы объеденились за {time.time()-t}")






