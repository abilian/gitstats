import os
import shlex
import subprocess
from pathlib import Path

from gitstats.main import main


def sh(cmd: list | str):
    if isinstance(cmd, str):
        cmd = shlex.split(cmd)
    print(f"Running: {cmd}")
    subprocess.run(cmd, check=True)


def test_help():
    sh("python -m gitstats.main --help")


def test_script():
    Path("tmp").mkdir(exist_ok=True)
    sh("python -m gitstats.main . tmp/report")
