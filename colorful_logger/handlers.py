#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: thepoy
# @Email: thepoy@163.com
# @File Name: handlers.py
# @Created: 2021-05-21 13:53:40
# @Modified: 2021-06-05 11:24:02

import logging

from logging import LogRecord
from logging.handlers import QueueHandler, QueueListener

from colorful_logger.formatter import ColorfulFormatter

LOG_FORMAT = "[%(levelname)s] %(asctime)s - %(name)s - %(pathname)s:%(lineno)d - %(message)s"
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def console_handler() -> logging.StreamHandler:
    console_handler = logging.StreamHandler()

    fmt = ColorfulFormatter(datefmt=TIME_FORMAT)
    console_handler.setFormatter(fmt)
    return console_handler


def file_handler(file_path: str, colorful: bool) -> logging.FileHandler:
    file_handler = logging.FileHandler(
        filename=file_path,
        mode="w",
        encoding="utf-8",
    )
    if colorful:
        fmt = ColorfulFormatter(datefmt=TIME_FORMAT)
    else:
        fmt = logging.Formatter(LOG_FORMAT, TIME_FORMAT)
    file_handler.setFormatter(fmt)
    return file_handler


class ColorfulQueueHandler(QueueHandler):
    # def __init__(self, queue):
    #     self.formatter = ColorfulFormatter(datefmt=TIME_FORMAT)
    #     super().__init__(queue)

    # def prepare(self, record: LogRecord) -> LogRecord:
    #     return super().prepare(record)
    pass


class ColorfulQueueListener(QueueListener):
    pass
