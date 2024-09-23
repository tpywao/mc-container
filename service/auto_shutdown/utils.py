from io import BufferedReader
from pathlib import Path


class LogReader:
    path: Path
    file: BufferedReader

    def __init__(self, path_str: str) -> None:
        self.path = Path(path_str)
        self.file = self.path.open("rb")

    def __del__(self):
        self.file.close()

    def seek_to_pre_2bytes(self):
        """
        現在の2バイトに戻る
        """
        self.file.seek(-2, 1)

    def seek_to_pre_line(self):
        """
        一つ前の行にseekする
        """
        self.seek_to_pre_2bytes()
        # 最新の改行を探す
        while self.file.read(1) != b"\n":
            self.seek_to_pre_2bytes()

    def seek_to_eof(self):
        """
        EOFにseekする
        """
        self.file.seek(0, 2)

    def seek_to_lastline(self):
        """
        最終行にseekする
        """
        self.seek_to_eof()
        self.seek_to_pre_line()

    def readlines(self):
        return self.file.readlines()
