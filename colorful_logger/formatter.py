#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: thepoy
# @Email: thepoy@163.com
# @File Name: formatter.py
# @Created: 2021-05-21 13:53:40
# @Modified: 2021-06-05 09:32:40

import time

from logging import Formatter, LogRecord

from colort import display_style as ds


class ColorfulFormatter(Formatter):
    """
    有颜色的日志
    """

    def __init__(self, fmt=None, datefmt=None, style="%"):
        self.default_color = "{0}"

        # fmt: off
        self.level_prefix = {
            "DEBUG"  : "[DEBUG] ",
            "INFO"   : "[INFO]  ",
            "WARN"   : "[WARN]  ",
            "WARNING": "[WARN]  ",
            "ERROR"  : "[ERROR] ",
            "FATAL"  : "[FATAL] ",
        }
        # fmt: on

        super().__init__(fmt, datefmt, style)

    def __level(self, levelname: str) -> str:
        if levelname == "DEBUG":
            return ds.format_with_one_style(self.level_prefix[levelname], ds.foreground_color.purple)

        if levelname == "INFO":
            return ds.format_with_one_style(self.level_prefix[levelname], ds.foreground_color.green)

        if levelname == "WARNING":
            return ds.format_with_one_style(self.level_prefix[levelname], ds.foreground_color.orange)

        if levelname == "ERROR":
            return ds.format_with_one_style(self.level_prefix[levelname], ds.foreground_color.red)

        if levelname == "FATAL":
            return ds.format_with_one_style(self.level_prefix[levelname], ds.foreground_color.red)

        if levelname == "CRITICAL":
            return ds.format_with_one_style(self.level_prefix["FATAL"], ds.foreground_color.red)

        return ds.format_with_one_style(f"[{levelname}]", ds.mode.normal)

    def __time(self, record):
        ct = self.converter(record.created)
        s = time.strftime(self.datefmt, ct)  # type: ignore

        return ds.format_with_one_style(s, ds.foreground_color.blue) + "  "

    def __name(self, record):
        return "" if record.name == "root" else ds.format_with_one_style(f"{record.name} - ", ds.foreground_color.cyan)

    def __position(self, record: LogRecord):
        if record.levelname in ["DEBUG", "INFO", "WARNING", "WARN"]:
            return ""
        return ds.format_with_one_style(f"{record.pathname}:{record.lineno}", ds.foreground_color.orange) + "\t"

    def format(self, record: LogRecord):
        record.message = record.getMessage()
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)

        msg = record.msg % record.args if record.args else record.msg
        s = self.__level(record.levelname) + self.__time(record) + self.__position(record) + self.__name(record) + msg
        return s
