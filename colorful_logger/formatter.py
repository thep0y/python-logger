#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author:    thepoy
# @Email:     thepoy@163.com
# @File Name: formatter.py
# @Created:   2021-05-21 13:53:40
# @Modified:  2022-03-10 11:15:22

import sys
import os

from datetime import datetime
from logging import Formatter, LogRecord
from typing import Dict, Optional, Tuple

if sys.version_info < (3, 8):
    from typing_extensions import Literal
else:
    from typing import Literal

from colort import display_style as ds
from colort.colort import Style
from colorful_logger.consts import TIME_FORMAT_WITHOUT_DATE

_style = Literal["%", "{", "$"]


class ColorfulFormatter(Formatter):
    """
    有颜色的日志
    """

    def __init__(
        self,
        fmt: Optional[str] = None,
        datefmt: Optional[str] = None,
        style: _style = "%",
        print_position=True,
        to_file=False,
    ):
        self.default_color = "{0}"
        self.print_position = print_position
        self.to_file = to_file

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
            return f"[{level[0]}] "

        return "%s%s%s " % (
            ds.format_with_one_style("[", ds.fc.light_gray),
            ds.format_with_one_style(level[0], level[1]),
            ds.format_with_one_style("]", ds.fc.light_gray),
        )

    def __time(self, record):
        assert isinstance(self.datefmt, str)

        t = datetime.fromtimestamp(record.created)
        s = (
            t.strftime(self.datefmt)[:-3]
            if self.datefmt == TIME_FORMAT_WITHOUT_DATE
            else t.strftime(self.datefmt)
        )

        if self.to_file:
            return s + " "

        return ds.format_with_one_style(s, ds.fc.dark_gray) + " "

    def __name(self, record):
        if self.to_file:
            return "" if record.name == "root" else f"{record.name} "

        return (
            ""
            if record.name == "root"
            else ds.format_with_one_style(f"{record.name} ", ds.fc.cyan)
        )

    def __position(self, record: LogRecord):
        if not self.print_position:
            return ""

        if record.levelname in ["INFO", "WARNING", "WARN"]:
            return ""

        if self.to_file:
            return f"{os.path.abspath(record.pathname)}:{record.lineno} "

        return (
            ds.format_with_one_style(
                f"{os.path.relpath(record.pathname)}:{record.lineno}", ds.mode.bold
            )
            + " "
        )

    @property
    def __connector(self):
        if self.to_file:
            return "- "

        return ds.format_with_one_style("-", ds.fc.light_cyan) + " "

    def format(self, record: LogRecord):
        record.message = record.getMessage()
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)

        msg = record.msg % record.args if record.args else record.msg

        if self.to_file:
            s = (
                self.__level(record.levelname)
                + self.__time(record)
                + self.__name(record)
                + self.__position(record)
                + self.__connector
                + msg
            )
        else:
            s = (
                self.__time(record)
                + self.__level(record.levelname)
                + self.__name(record)
                + self.__position(record)
                + self.__connector
                + msg
            )

        return s
