import os
from pathlib import Path

DEBUG = True

ROOT_PATH = Path(os.path.dirname(os.path.abspath(__file__)))

"""Для правильной работы FFMPEG"""
FFMPEG_PATH = ROOT_PATH.joinpath(r"ffmpeg_mini\bin")
os.environ["PATH"] += os.pathsep + FFMPEG_PATH.__str__()

"Конфиги"
SAVE_PATH = ROOT_PATH.joinpath("save")
