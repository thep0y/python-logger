#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author:      thepoy
# @Email:       thepoy@163.com
# @File Name:   types.py
# @Created At:  2023-02-07 13:08:55
# @Modified At: 2023-02-21 10:42:59
# @Modified By: thepoy

from os import PathLike
from typing import Union

StrPath = Union[str, PathLike[str]]
