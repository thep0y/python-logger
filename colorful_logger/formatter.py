#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: thepoy
# @Email: thepoy@163.com
# @File Name: formatter.py
# @Created: 2021-05-21 13:53:40
# @Modified: 2021-05-22 11:07:16

import time

from logging import Formatter, LogRecord


class ColorfulFormatter(Formatter):
    """
    有颜色的日志
    """
    def __init__(self, fmt=None, datefmt=None, style='%'):
        self.default_color = "{0}"

        self.colors = {
            "off": "{0}",
            "red": "\033[0;31m{0}\033[0m",
            "green": "\033[0;32m{0}\033[0m",
            "orange": "\033[0;33m{0}\033[0m",
            "blue": "\033[0;34m{0}\033[0m",
            "purple": "\033[0;35m{0}\033[0m",
            "cyan": "\033[0;36m{0}\033[0m",
            "gray": "\033[0;37m{0}\033[0m",
        }

        self.level_prefix = {
            "DEBUG": "[DEBUG] ",
            "INFO": "[INFO]  ",
            "WARN": "[WARN]  ",
            "WARNING": "[WARN]  ",
            "ERROR": "[ERROR] ",
            "FATAL": "[FATAL] ",
        }

        # self.datefmt = datefmt

        super().__init__(fmt, datefmt, style)

    def __level(self, levelname: str) -> str:
        if levelname == "DEBUG":
            return self.colors["purple"].format(self.level_prefix[levelname])

        if levelname == "INFO":
            return self.colors["green"].format(self.level_prefix[levelname])

        if levelname == "WARNING":
            return self.colors["orange"].format(self.level_prefix[levelname])

        if levelname == "ERROR":
            return self.colors["red"].format(self.level_prefix[levelname])

        if levelname == "FATAL":
            return self.colors["red"].format(self.level_prefix[levelname])

        if levelname == "CRITICAL":
            return self.colors["red"].format(self.level_prefix["FATAL"])

        return self.colors["off"].format(levelname)

    def __time(self, record):
        ct = self.converter(record.created)
        s = time.strftime(self.datefmt, ct)

        return self.colors["blue"].format(s) + "  "

    def __name(self, record):
        return "" if record.name == "root" else self.colors["cyan"].format(f"{record.name} - ")

    def __position(self, record: LogRecord):
        if record.levelname in ["DEBUG", "INFO", "WARNING", "WARN"]:
            return ""
        return self.colors["orange"].format(f"{record.pathname}:{record.lineno}") + "  "

    def format(self, record: LogRecord):
        record.message = record.getMessage()
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)
        s = self.formatMessage(record)
        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            if s[-1:] != "\n":
                s = s + "\n"
            s = s + record.exc_text
        if record.stack_info:
            if s[-1:] != "\n":
                s = s + "\n"
            s = s + self.formatStack(record.stack_info)

        s = self.__level(
            record.levelname) + self.__time(record) + self.__position(record) + self.__name(record) + record.msg
        return s
