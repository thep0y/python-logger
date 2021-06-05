#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: thepoy
# @Email: thepoy@163.com
# @File Name: logger.py
# @Created: 2021-05-21 13:53:40
# @Modified: 2021-06-05 20:08:56

from logging.handlers import QueueListener
import os
import sys
import logging
import queue

from typing import Optional
from logging import Logger

from colorful_logger.handlers import ColorfulQueueHandler, ColorfulQueueListener, console_handler, file_handler

NOTSET = logging.NOTSET
DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
FATAL = logging.FATAL
CRITICAL = logging.CRITICAL

LOG_FORMAT = "[%(levelname)s] %(asctime)s - %(name)s - %(pathname)s:%(lineno)d - %(message)s"
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

default_level = WARNING

if os.environ.get("DEBUG"):
    default_level = DEBUG


class ColorfulLogger(Logger):
    def addListener(self, listener: QueueListener):
        self.listener = listener

    def fatal(self, msg, *args, **kwargs):
        if self.isEnabledFor(logging.FATAL):
            self._log(logging.FATAL, msg, args, **kwargs)
            sys.exit(1)

    def __enter__(self):
        self.listener.start()
        return self

    def __exit__(self, type, value, trace):
        self.listener.stop()


def get_logger(
    name: Optional[str] = None,
    level: int = default_level,
    show: bool = True,
    file_path: Optional[str] = None,
    file_colorful: bool = False,
) -> ColorfulLogger:
    """Return a colorful logger with the specified name, creating it if necessary.

    If no name is specified, return the root logger.

    Args:
        name (Optional[str], optional): logger name.
        level (str, None): The logging level of this logger, default level is WARNING.
        show (bool, True): Whether the log is displayed in the terminal, default is True.
        file_path (str, None): When 'file_path' is not None, the log will be saved to 'file_path'.
        file_colorful (bool, False): Whether the log file is in color, the default is False.

    Returns:
        ColorfulLogger: logger
    """

    if not file_path and not show:
        raise NotImplementedError("the log must be displayed in the terminal or saved to a file")

    name = name if name else "root"
    logger = ColorfulLogger(name)

    q = queue.Queue(-1)  # no limit on size
    queue_handler = ColorfulQueueHandler(q)
    logger.addHandler(queue_handler)

    logger.setLevel(level)

    handlers = []
    if show:
        handlers.append(console_handler())
    if file_path:
        handlers.append(file_handler(file_path, file_colorful))

    listener = ColorfulQueueListener(
        q,
        *handlers,
    )

    logger.addListener(listener)

    return logger


logger = get_logger()


def child_logger(name: str, logger: ColorfulLogger = logger) -> ColorfulLogger:
    """Generate a child logger through the incoming logger

    Args:
        name (str): child logger name
        logger (Logger, optional): parent logger, default is the logger generated by the get_logger function

    Returns:
        ColorfulLogger: child logger
    """

    lc = ColorfulLogger(name)
    lc.level = logger.level
    lc.handlers = logger.handlers
    lc.listener = logger.listener
    # lc.propagate = False
    return lc
