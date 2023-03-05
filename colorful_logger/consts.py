#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author:      thepoy
# @Email:       thepoy@163.com
# @File Name:   consts.py
# @Created At:  2022-02-20 13:45:21
# @Modified At: 2023-03-05 15:24:57
# @Modified By: thepoy

import logging
import os

from pathlib import Path

TRACE = 5
DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
FATAL = logging.FATAL
CRITICAL = logging.CRITICAL

TIME_FORMAT_WITH_DATE = "%Y-%m-%d %H:%M:%S"
TIME_FORMAT_WITHOUT_DATE = "%H:%M:%S.%f"

LOG_FORMAT = (
    "[%(levelname)s] %(asctime)s - %(name)s - %(pathname)s:%(lineno)d - %(message)s"
)

BASE_DIR = Path(os.path.dirname(__file__))
