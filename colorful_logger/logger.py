#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: thepoy
# @Email: thepoy@163.com
# @File Name: logger.py
# @Created: 2021-05-21 13:53:40
# @Modified: 2021-05-22 11:24:33

import sys
import logging

from typing import Optional
from logging import Logger

from colorful_logger.formatter import ColorfulFormatter

NOTSET = logging.NOTSET
DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
FATAL = logging.FATAL
CRITICAL = logging.CRITICAL

LOG_FORMAT = '[%(levelname)s] %(asctime)s - %(name)s - %(pathname)s:%(lineno)d - %(message)s'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def __console_handler(logger):
    console_handler = logging.StreamHandler()

    fmt = ColorfulFormatter(datefmt=TIME_FORMAT)
    console_handler.setFormatter(fmt)
    logger.addHandler(console_handler)


def __file_handler(logger, file_path):
    file_handler = logging.FileHandler(
        filename=file_path,
        mode="w",
        encoding="utf-8",
    )

    fmt = logging.Formatter(LOG_FORMAT, TIME_FORMAT)
    file_handler.setFormatter(fmt)
    logger.addHandler(file_handler)


class CustomLogger(Logger):
    def fatal(self, msg, *args, **kwargs):
        if self.isEnabledFor(logging.FATAL):
            self._log(logging.FATAL, msg, args, **kwargs)
        sys.exit(1)


def get_logger(
    name: Optional[str] = None,
    level: int = WARNING,
    show: bool = True,
    file_path: Optional[str] = None,
) -> Logger:
    """Return a colorful logger with the specified name, creating it if necessary.

    If no name is specified, return the root logger.

    Args:
        level (str, None): The logging level of this logger, default level is WARNING.
        show (bool, True): Whether the log is displayed in the terminal, default is True.
        file_path (str, None): When 'file_path' is not None, the log will be saved to 'file_path'.
    """
    if not file_path and not show:
        raise NotImplementedError("the log must be displayed in the terminal or saved to a file")

    name = name if name else "root"

    logger = CustomLogger(name)
    logger.setLevel(level)

    if show:
        __console_handler(logger)

    if file_path:
        __file_handler(logger, file_path)

    return logger


# The log is only output to the terminal by default logger.
logger = get_logger()
