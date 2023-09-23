import os
from pathlib import Path

ROOT_PATH = Path(os.path.dirname(os.path.abspath(__file__)))

"""Для правильной работы PyDub"""
FFMPEG_PATH = ROOT_PATH.joinpath(r"ffmpeg\bin")
os.environ["PATH"] += os.pathsep + FFMPEG_PATH.__str__()

