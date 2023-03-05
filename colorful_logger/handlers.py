#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author:      thepoy
# @Email:       thepoy@163.com
# @File Name:   handlers.py
# @Created At:  2021-05-21 13:53:40
# @Modified At: 2023-03-05 14:50:44
# @Modified By: thepoy

import logging

from logging.handlers import QueueHandler, QueueListener
from colorful_logger.formatter import ColorfulFormatter
from colorful_logger.types import StrPath


def console_handler(
    datefmt: str, add_file_path=True, disable_line_number_filter=False
) -> logging.StreamHandler:
    console_handler = logging.StreamHandler()

    fmt = ColorfulFormatter(
        datefmt=datefmt,
        add_file_path=add_file_path,
        disable_line_number_filter=disable_line_number_filter,
    )
    console_handler.setFormatter(fmt)
    return console_handler


def file_handler(
    file_path: StrPath,
    colorful: bool,
    datefmt: str,
    add_file_path=True,
    disable_line_number_filter=False,
) -> logging.FileHandler:
    file_handler = logging.FileHandler(
        filename=file_path,
        mode="w",
        encoding="utf-8",
    )
    if colorful:
        fmt = ColorfulFormatter(
            datefmt=datefmt,
            add_file_path=add_file_path,
            disable_line_number_filter=disable_line_number_filter,
        )
    else:
        fmt = ColorfulFormatter(
            datefmt=datefmt,
            add_file_path=add_file_path,
            to_file=True,
            disable_line_number_filter=disable_line_number_filter,
        )
    file_handler.setFormatter(fmt)
    return file_handler


class ColorfulQueueHandler(QueueHandler):
    pass


class ColorfulQueueListener(QueueListener):
    pass
