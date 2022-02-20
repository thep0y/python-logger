#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author:    thepoy
# @Email:     thepoy@163.com
# @File Name: consts.py
# @Created:   2022-02-20 13:45:21
# @Modified:  2022-02-20 14:24:54

import logging

NOTSET = logging.NOTSET
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
