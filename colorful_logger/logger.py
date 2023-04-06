#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author:      thepoy
# @Email:       thepoy@163.com
# @File Name:   logger.py
# @Created At:  2021-05-21 13:53:40
# @Modified At: 2023-04-06 16:09:03
# @Modified By: thepoy

import os
import sys
import queue
import warnings

from types import TracebackType
from typing import Any, List, NoReturn, Optional, Tuple, Union, Mapping, Type, Dict
from logging import Logger, Handler, _srcfile, addLevelName
from logging.handlers import QueueListener
from colorful_logger.types import StrPath

from colorful_logger.handlers import (
    ColorfulQueueHandler,
    ColorfulQueueListener,
    console_handler,
    file_handler,
)
from colorful_logger.consts import (
    DEBUG,
    TRACE,
    WARNING,
    ERROR,
    FATAL,
    INFO,
    TIME_FORMAT_WITHOUT_DATE,
)


default_level = WARNING


_env_levels = {
    "0": FATAL,
    "1": ERROR,
    "2": WARNING,
    "3": INFO,
    "4": DEBUG,
    "5": TRACE,
}


def get_level_from_env(default_level=WARNING):
    level = os.getenv("LOG_LEVEL")
    if not level:
        return default_level

    return _env_levels.get(level, default_level)


def is_debug() -> bool:
    v = os.getenv("DEBUG")

    if not v or v == "0" or v.lower() == "false":
        return False

    if v == "1" or v.lower() == "true":
        return True

    return False


if is_debug():
    default_level = DEBUG


_SysExcInfoType = Union[
    Tuple[Type[BaseException], BaseException, Optional[TracebackType]],
    Tuple[None, None, None],
]
_ExcInfoType = Union[_SysExcInfoType, BaseException]


class ColorfulLogger(Logger):
    def __init__(self, name: str, level: int = 0) -> None:
        super().__init__(name, level)
        addLevelName(TRACE, "TRACE")
        addLevelName(FATAL, "FATAL")

    def addListener(self, listener: QueueListener):
        self.listener = listener

    def _log(
        self,
        level: int,
        msg: str,
        exc_info: Optional[_ExcInfoType] = None,
        extra: Optional[Mapping[str, Any]] = None,
        stack_info: bool = False,
        stacklevel: int = 3,
        kwargs: Dict[str, Any] = {},
    ):
        """
        Low-level logging routine which creates a LogRecord and then calls
        all the handlers of this logger to handle the record.
        """
        sinfo = None
        if _srcfile:
            # IronPython doesn't track Python frames, so findCaller raises an
            # exception on some versions of IronPython. We trap it here so that
            # IronPython can use logging.
            try:
                if sys.version_info >= (3, 8):
                    fn, lno, func, sinfo = self.findCaller(stack_info, stacklevel)
                else:
                    fn, lno, func, sinfo = self.findCaller(stack_info)
            except ValueError:  # pragma: no cover
                fn, lno, func = "(unknown file)", 0, "(unknown function)"
        else:  # pragma: no cover
            fn, lno, func = "(unknown file)", 0, "(unknown function)"
        if exc_info:
            if isinstance(exc_info, BaseException):
                exc_info = (type(exc_info), exc_info, exc_info.__traceback__)
            elif not isinstance(exc_info, tuple):
                exc_info = sys.exc_info()

        record = self.makeRecord(
            self.name, level, fn, lno, msg, {}, exc_info, func, extra, sinfo
        )
        record.kwargs = kwargs

        self.handle(record)

    def fatal(self, msg: str, **kwargs: Any) -> NoReturn:
        """
        Log msg and kwargs with severity 'FATAL'.

        logger.fatal("got student failed", err="something error", status_code=403)
        """
        if self.isEnabledFor(FATAL):
            self._log(FATAL, msg, kwargs=kwargs)
        sys.exit(1)

    def info(self, msg: str, **kwargs: Any):
        """
        Log msg and kwargs with severity 'INFO'.

        logger.info("got a student", id=1, name="Tommy")
        """
        if self.isEnabledFor(INFO):
            self._log(INFO, msg, kwargs=kwargs)

    def debug(self, msg: str, **kwargs: Any):
        """
        Log msg and kwargs with severity 'DEBUG'.

        logger.debug("got a student", id=1, name="Tommy")
        """
        if self.isEnabledFor(DEBUG):
            self._log(DEBUG, msg, kwargs=kwargs)

    def warning(self, msg: str, **kwargs: Any):
        """
        Log msg and kwargs with severity 'WARNING'.

        logger.warning("got a student without name", id=1)
        """
        if self.isEnabledFor(WARNING):
            self._log(WARNING, msg, kwargs=kwargs)

    def error(self, msg: str, **kwargs: Any):
        """
        Log msg and kwargs with severity 'ERROR'.

        logger.error("got student failed", err="something error", status_code=403)
        """
        if self.isEnabledFor(ERROR):
            self._log(ERROR, msg, kwargs=kwargs)

    def trace(self, msg: str, **kwargs: Any):
        """
        Log msg and kwargs with severity 'TRACE'.

        logger.trace("got a student", id=1, name="Tommy")
        """
        if self.isEnabledFor(TRACE):
            self._log(TRACE, msg, kwargs=kwargs)

    def __enter__(self):
        if hasattr(self, "listener"):
            self.listener.start()
        else:
            warnings.warn(
                "do not use the with statement when using synchronous mode",
                SyntaxWarning,
            )

        return self

    def __exit__(self, *args):
        if hasattr(self, "listener"):
            self.listener.stop()

    def child(self, name: str) -> "ColorfulLogger":
        lc = ColorfulLogger(name)
        lc.level = self.level
        lc.handlers = self.handlers

        if hasattr(self, "listener"):
            lc.listener = self.listener

        return lc


def get_logger(
    name: Optional[str] = None,
    level: int = default_level,
    datefmt: str = TIME_FORMAT_WITHOUT_DATE,
    show: bool = True,
    file_path: Optional[StrPath] = None,
    file_colorful: bool = False,
    add_file_path: bool = True,
    disable_line_number_filter: bool = False,
    asynchronous: bool = True,
) -> ColorfulLogger:
    """Return a colorful logger with the specified name, creating it if necessary.

    If no name is specified, return the root logger.

    Args:
        name (Optional[str], optional): logger name.
        level (str, None): The logging level of this logger, default level is WARNING.
        show (bool, True): Whether the log is displayed in the terminal, default is True.
        file_path (str, None): When 'file_path' is not None, the log will be saved to 'file_path'.
        file_colorful (bool, False): Whether the log file is in color, the default is False.
        add_file_path (bool, True): Whether to add the path of the calling file, the default is False.
        disable_line_number_filter (bool, False): Whether to add the number of calling line in all levels of logs, the default is False.
        asynchronous (bool, true):  Whether to use asynchronous mode for logging, the default is True.

    Returns:
        ColorfulLogger: logger
    """

    if not file_path and not show:
        raise NotImplementedError(
            "the log must be displayed in the terminal or saved to a file"
        )

    name = name if name else "root"
    logger = ColorfulLogger(name)

    logger.setLevel(level)

    handlers: List[Handler] = []
    if show:
        handlers.append(
            console_handler(
                datefmt,
                add_file_path=add_file_path,
                disable_line_number_filter=disable_line_number_filter,
            )
        )
    if file_path:
        handlers.append(
            file_handler(
                file_path,
                file_colorful,
                datefmt,
                add_file_path=add_file_path,
                disable_line_number_filter=disable_line_number_filter,
            )
        )

    if asynchronous:
        q = queue.Queue(-1)  # no limit on size
        queue_handler = ColorfulQueueHandler(q)
        logger.addHandler(queue_handler)

        listener = ColorfulQueueListener(
            q,
            *handlers,
        )

        logger.addListener(listener)
    else:
        logger.handlers = handlers

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

    return logger.child(name)
