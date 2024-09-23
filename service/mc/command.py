from io import TextIOWrapper
from pathlib import Path


class Command:
    """
    マイクラサーバコマンド

    https://minecraft.fandom.com/wiki/Commands
    """

    pipe_path: Path
    file: TextIOWrapper

    def __init__(self, pipe_str: str):
        self.pipe_path = Path(pipe_str)
        self.file = self.pipe_path.open("w")

    def __del__(self):
        self.file.close()

    def run(self, command):
        self.file.write(f"{command}\n")
        self.file.flush()

    def list(self):
        """
        サーバー上のプレイヤーの一覧を表示
        """
        self.run("list")

    def say(self, message: str):
        """
        サーバー上のすべてのプレイヤーにメッセージを送信
        """
        self.run(f"say {message}")

    def stop(self):
        """
        ワールドの変更を保存してサーバを停止
        """
        self.run("stop")

    def prepare_backup(self):
        """
        バックアップ準備

        - サーバの変更をファイルに反映
        - 以降の変更はファイルに反映しない(save resumeで再開)
        """
        self.run("save hold")

    def query_backup(self):
        """
        バックアップ状態の確認

        done: Data saved. Files are now ready to be copied.
        waiting: A previous save has not been completed.
        """
        self.run(command="save query")

    def resume_buckup(self):
        """
        バックアップ準備
        """
        self.run("save resume")
