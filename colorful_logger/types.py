#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author:    thepoy
# @Email:     thepoy@163.com
# @File Name: types.py
# @Created:   2023-02-07 13:08:55
# @Modified:  2023-02-21 09:14:52

from os import PathLike
from typing import Union

StrPath = Union[str, PathLike[str]]
