#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author:      thepoy
# @Email:       thepoy@163.com
# @File Name:   formatter.py
# @Created At:  2021-05-21 13:53:40
# @Modified At: 2023-02-21 12:54:51
# @Modified By: thepoy

import sys
import os

from datetime import datetime
from logging import Formatter, LogRecord
from typing import Dict, Optional, Tuple

if sys.version_info < (3, 8):
    from typing_extensions import Literal, Final
else:
    from typing import Literal, Final

from colort import display_style as ds
from colort.colort import Style
from colorful_logger.consts import TIME_FORMAT_WITHOUT_DATE

_style = Literal["%", "{", "$"]

TimeSpec = Final[
    Literal["auto", "hours", "minutes", "seconds", "milliseconds", "microseconds"]
]


def _format_time(hh: int, mm: int, ss: int, us: int, timespec: TimeSpec = "auto"):
    specs = {
        "hours": "{:02d}",
        "minutes": "{:02d}:{:02d}",
        "seconds": "{:02d}:{:02d}:{:02d}",
        "milliseconds": "{:02d}:{:02d}:{:02d}.{:03d}",
        "microseconds": "{:02d}:{:02d}:{:02d}.{:06d}",
    }

    if timespec == "auto":
        # Skip trailing microseconds when us==0.
        timespec = "microseconds" if us else "seconds"
    elif timespec == "milliseconds":
        us //= 1000
    try:
        fmt = specs[timespec]
    except KeyError:
        raise ValueError("Unknown timespec value")
    else:
        return fmt.format(hh, mm, ss, us)


class ColorfulFormatter(Formatter):
    """
    有颜色的日志
    """

    def __init__(
        self,
        fmt: Optional[str] = None,
        datefmt: Optional[str] = None,
        style: _style = "%",
        add_file_path=False,
        to_file=False,
        disable_line_number_filter=False,
    ):
        self.default_color = "{0}"
        self.add_file_path = add_file_path
        self.to_file = to_file
        self.disable_line_number_filter = disable_line_number_filter

        self.level_config: Dict[str, Tuple[str, Style]] = {
            "DEBUG": ("DEB", ds.fc.purple),
            "INFO": ("INF", ds.fc.green),
            "WARN": ("WAR", ds.fc.yellow),
            "WARNING": ("WAR", ds.fc.yellow),
            "ERROR": ("ERR", ds.fc.light_red),
            "FATAL": ("FAT", ds.fc.red),
            "CRITICAL": ("FAT", ds.fc.red),
        }

        super().__init__(fmt, datefmt, style)

    def __level(self, levelname: str):
        level = self.level_config[levelname]

        if self.to_file:
            return f"[{level[0]}]"

        return ds.format_with_one_style(level[0], level[1])

    def __time(self, record):
        assert isinstance(self.datefmt, str)

        t = datetime.fromtimestamp(record.created)
        s = (
            _format_time(t.hour, t.minute, t.second, t.microsecond, "milliseconds")
            if self.datefmt == TIME_FORMAT_WITHOUT_DATE
            else t.strftime(self.datefmt)
        )

        if self.to_file:
            return s

        return ds.format_with_one_style(s, ds.fc.dark_gray)

    def __name(self, record: LogRecord):
        if self.to_file:
            return "" if record.name == "root" else f"{record.name}"

        return (
            ""
            if record.name == "root"
            else ds.format_with_one_style(f"{record.name}", ds.fc.cyan)
        )

    def __file_path(self, record: LogRecord):
        if not self.add_file_path:
            return ""

        if self.to_file:
            return os.path.abspath(record.pathname)

        if sys.platform == "win32":
            # Windows 上当 os.path.relpath 的 path 和 start
            # 不在一个分区上时会报 ValueError 错误，且没有完美的解决
            # 办法，使用绝对路径暂替。

            cur_dir = os.path.abspath(os.curdir)

            # windows 上允许的盘符是 26 个英文字母，所以只需对比绝对
            # 路径的第一个字母就可以判断是否跨区。
            if cur_dir[0] == record.pathname[0]:
                path = ds.format_with_one_style(
                    os.path.relpath(record.pathname), ds.mode.bold
                )
            else:
                path = ds.format_with_one_style(
                    os.path.abspath(record.pathname), ds.mode.bold
                )
        else:
            path = ds.format_with_one_style(
                os.path.relpath(record.pathname), ds.mode.bold
            )

        return path

    def __line_number(self, record: LogRecord):
        if not self.disable_line_number_filter and record.levelname in [
            "INFO",
            "WARNING",
            "WARN",
        ]:
            return ""

        if not self.add_file_path and record.name == "root":
            return ""

        if self.to_file:
            return f":{record.lineno}"

        return ds.format_with_one_style(f":{record.lineno}", ds.mode.bold)

    @property
    def __connector(self):
        if self.to_file:
            return "-"

        return ds.format_with_one_style("-", ds.fc.light_cyan)

    def format(self, record: LogRecord):
        record.message = record.getMessage()
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)

        msg = record.msg % record.args if record.args else record.msg

        if self.to_file:
            fields = (
                self.__level(record.levelname),
                self.__time(record),
                self.__name(record),
                self.__file_path(record),
                self.__line_number(record),
                self.__connector,
                msg,
            )
        else:
            fields = (
                self.__time(record),
                self.__level(record.levelname),
                self.__name(record),
                self.__file_path(record),
                self.__line_number(record),
                self.__connector,
                msg,
            )

        texts = [
            " " + fields[i] if i > 0 and fields[i] and i != 4 else fields[i]
            for i in range(len(fields))
        ]

        return "".join(texts)
