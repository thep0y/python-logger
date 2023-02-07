#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author:    thepoy
# @Email:     thepoy@163.com
# @File Name: __init__.py
# @Created:   2021-05-21 13:53:40
# @Modified:  2023-02-07 13:22:19

from colorful_logger.logger import (
    get_logger,
    logger,
    child_logger,
)
from colorful_logger.consts import DEBUG, INFO, WARNING, ERROR, FATAL

__all__ = [
    "logger",
    "get_logger",
    "child_logger",
    "DEBUG",
    "INFO",
    "WARNING",
    "ERROR",
    "FATAL",
]
