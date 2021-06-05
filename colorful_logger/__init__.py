#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: thepoy
# @Email: thepoy@163.com
# @File Name: __init__.py
# @Created: 2021-05-21 13:53:40
# @Modified: 2021-06-05 09:37:07

from colorful_logger.logger import logger, get_logger, child_logger, basic_logger

__all__ = ["logger", "get_logger", "child_logger", "basic_logger"]

__version__ = "0.0.9"
