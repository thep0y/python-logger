#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author:    thepoy
# @Email:     thepoy@163.com
# @File Name: formatter.py
# @Created:   2021-05-21 13:53:40
# @Modified:  2022-02-20 14:18:31

import os

from datetime import datetime
from logging import Formatter, LogRecord
from typing import Dict, Literal, Optional, Tuple

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
    ):
        self.default_color = "{0}"

        self.level_config: Dict[str, Tuple[str, Style]] = {
            "DEBUG": ("DEB", ds.fc.purple),
            "INFO": ("INF", ds.fc.green),
            "WARN": ("WAR", ds.fc.yellow),
            "WARNING": ("WAR", ds.fc.yellow),
            "ERROR": ("ERR", ds.fc.light_red),
            "FATAL": ("FAT", ds.fc.red),
        }

        super().__init__(fmt, datefmt, style)

    def __level(self, levelname: str):
        level = self.level_config[levelname]
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

        return ds.format_with_one_style(s, ds.fc.dark_gray) + " "

    def __name(self, record):
        return (
            ""
            if record.name == "root"
            else ds.format_with_one_style(f"{record.name} ", ds.fc.cyan)
        )

    def __position(self, record: LogRecord):
        if record.levelname in ["INFO", "WARNING", "WARN"]:
            return ""
        return (
            ds.format_with_one_style(
                f"{os.path.relpath(record.pathname)}:{record.lineno}", ds.mode.bold
            )
            + " "
        )

    @property
    def __connector(self):
        return ds.format_with_one_style("-", ds.fc.light_cyan) + " "

    def format(self, record: LogRecord):
        record.message = record.getMessage()
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)

        msg = record.msg % record.args if record.args else record.msg
        s = (
            self.__time(record)
            + self.__level(record.levelname)
            + self.__name(record)
            + self.__position(record)
            + self.__connector
            + msg
        )
        return s
