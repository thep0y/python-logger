#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: thepoy
# @Email: thepoy@163.com
# @File Name: __init__.py
# @Created: 2021-05-21 13:53:40
# @Modified: 2021-06-05 19:03:16

# from colorful_logger.logger import logger, get_logger, child_logger, basic_logger

# __all__ = ["logger", "get_logger", "child_logger", "basic_logger"]

from colorful_logger.logger import get_logger, logger, child_logger
__all__ = ["logger", "get_logger", "child_logger"]

__version__ = "0.1.0"
