#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author:    thepoy
# @Email:     thepoy@163.com
# @File Name: handlers.py
# @Created:   2021-05-21 13:53:40
# @Modified:  2022-03-25 10:06:16

import logging

from logging.handlers import QueueHandler, QueueListener
from colorful_logger.formatter import ColorfulFormatter


def console_handler(datefmt: str, print_position=True) -> logging.StreamHandler:
    console_handler = logging.StreamHandler()

    fmt = ColorfulFormatter(datefmt=datefmt, print_position=print_position)
    console_handler.setFormatter(fmt)
    return console_handler


def file_handler(
    file_path: str, colorful: bool, datefmt: str, print_position=True
) -> logging.FileHandler:
    file_handler = logging.FileHandler(
        filename=file_path,
        mode="w",
        encoding="utf-8",
    )
    if colorful:
        fmt = ColorfulFormatter(datefmt=datefmt, print_position=print_position)
    else:
        fmt = ColorfulFormatter(
            datefmt=datefmt, print_position=print_position, to_file=True
        )
    file_handler.setFormatter(fmt)
    return file_handler


class ColorfulQueueHandler(QueueHandler):
    pass


class ColorfulQueueListener(QueueListener):
    pass
