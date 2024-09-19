#!/usr/bin/env python3

from argparse import ArgumentParser
from io import BufferedReader, TextIOWrapper
from time import sleep
import os
import re
from pathlib import Path


class McCmd:
    """
    マイクラサーバコマンド
    """

    pipe_path: Path
    file: TextIOWrapper

    def __init__(self, pipe_str: str):
        self.pipe_path = Path(pipe_str)
        self.file = self.pipe_path.open("w")

    def __del__(self):
        self.file.close()

    def list(self):
        self.file.write("list\n")

    def say(self, message: str):
        self.file.write(f"say {message}\n")

    def stop(self):
        """
        ワールドの変更を保存してサーバを終了
        """
        self.file.write("stop\n")


class TailHandler:
    path: Path
    file: BufferedReader

    def __init__(self, path_str: str) -> None:
        self.path = Path(path_str)
        self.file = self.path.open("rb")
        self.seek_lastline()
        self.seek_pre_line()

    def __del__(self):
        self.file.close()

    def seek_pre_2bytes(self):
        """
        現在の2バイトに戻る
        """
        self.file.seek(-2, 1)

    def seek_lastline(self):
        """
        最終行にseekする
        """
        # EOFに移動
        self.file.seek(0, 2)
        self.seek_pre_line()

    def seek_pre_line(self):
        """
        一つ前の行にseekする
        """

        self.seek_pre_2bytes()
        # 最新の改行を探す
        while self.file.read(1) != b"\n":
            self.seek_pre_2bytes()

    def readlines(self):
        return self.file.readlines()


def has_active_user(tail: TailHandler):
    pattern: re.Pattern[str] = re.compile(
        r"There are (?P<active>[\d]+)/[\d]+", re.ASCII
    )
    lines = tail.readlines()
    for line in reversed(lines):
        result = pattern.search(line.decode())
        if result is None:
            continue

        active = result.group("active")
        if int(active) == 0:
            return False
    return True


def main():
    parser = ArgumentParser()
    parser.add_argument("service_name", type=str)
    args = parser.parse_args()

    service_name = args.service_name
    path_str = f"/var/log/mc@{service_name}.log"
    pipe_str = f"/var/run/mc@{service_name}"

    cmd = McCmd(pipe_str)
    cmd.list()

    tail = TailHandler(path_str)
    has_active = has_active_user(tail)

    if not has_active:
        cmd.say("5分後にサーバを終了します")
        sleep(60 * 5)
        cmd.stop()
        sleep(30)
        os.system("sudo shutdown -h now")


main()
