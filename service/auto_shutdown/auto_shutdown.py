#!/usr/bin/env python3

"""
1. サーバ上のアクティブユーザがいるか確認
2. いなければ
    - MCサーバを停止する
    - データバックアップを行う
    - マシンを終了する
"""

from argparse import ArgumentParser
from time import sleep
import os
import re
from logging import getLogger, DEBUG, INFO, WARNING


from ..mc.command import Command as McCommand
from .utils import LogReader


logger = getLogger(__name__)


LOGLEVEL_MAP = [
    DEBUG,
    INFO,
    WARNING,
]


def parse_args():
    pipe_path_template = "/var/run/mc@{service_name}"
    log_path_template = "/var/log/mc@{service_name}.log"

    parser = ArgumentParser()
    parser.add_argument("-v", "--verbose", type=int,
                        choices=(0, 1, 2), default=1)
    parser.add_argument("-n", "--dry-run", type=bool, action="store_true")

    parser.add_argument("service_name", type=str)
    parser.add_argument("--pipe", type=str)
    parser.add_argument("--log", type=str)
    args = parser.parse_args()

    service_name = args.service_name
    pipe_path_str = args.pipe
    if pipe_path_str is None:
        pipe_path_str = pipe_path_template.format(service_name=service_name)
    log_path_str = args.log
    if log_path_str is None:
        log_path_str = log_path_template.format(service_name=service_name)

    return {
        "pipe_path_str": pipe_path_str,
        "log_path_str": log_path_str,
        "log_level": LOGLEVEL_MAP[args.verbose]
    }


def has_active_user(log: LogReader):
    pattern: re.Pattern[str] = re.compile(
        r"There are (?P<active>[\d]+)/[\d]+", re.ASCII
    )
    lines = log.readlines()
    for line in reversed(lines):
        decoded = line.decode()
        logger.info(decoded)

        result = pattern.search(decoded)
        if result is None:
            continue

        active = result.group("active")
        if int(active) == 0:
            return False
    return True


def main(pipe_path_str, log_path_str):
    cmd = McCommand(pipe_path_str)
    log = LogReader(log_path_str)
    log.seek_to_eof()

    cmd.list()
    has_active = has_active_user(log)

    if not has_active:
        logger.info("Exit mc server on 30s")
        cmd.say("30秒後にサーバを終了します")
        sleep(30)
        cmd.stop()
        logger.info("Shutdown server on 30s")
        # mcサーバの終了まで30秒待つ
        sleep(30)
        # TODO: ここでバックアップもしたい
        os.system("sudo shutdown -h now")
    else:
        logger.info("Remain Active User")


if __name__ == "__main__":
    kwargs = parse_args()

    logger.setLevel(kwargs["log_level"])
    main(**kwargs)
