#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author:      thepoy
# @Email:       thepoy@163.com
# @File Name:   types.py
# @Created At:  2023-02-07 13:08:55
# @Modified At: 2023-03-06 19:34:50
# @Modified By: thepoy

from typing import Any, Dict, Optional, Union
from pathlib import Path
from logging import LogRecord

StrPath = Union[str, Path]


class Record(LogRecord):
    args: Dict[str, Any] = {}
