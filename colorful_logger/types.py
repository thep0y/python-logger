#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author:      thepoy
# @Email:       thepoy@163.com
# @File Name:   types.py
# @Created At:  2023-02-07 13:08:55
# @Modified At: 2023-03-06 20:08:37
# @Modified By: thepoy

from typing import Any, Dict, Union
from pathlib import Path
from logging import LogRecord

StrPath = Union[str, Path]


class Record(LogRecord):
    kwargs: Dict[str, Any] = {}
