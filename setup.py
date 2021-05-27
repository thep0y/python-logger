#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: thepoy
# @Email: thepoy@163.com
# @File Name: setup.py
# @Created: 2021-05-21 13:53:40
# @Modified: 2021-05-27 09:30:08

import codecs
import colorful_logger

from setuptools import setup, find_packages

with codecs.open("README.md", "r", "utf-8") as fd:
    setup(
        name="colorful-logger",
        version=colorful_logger.__version__,
        description='''
        A colorful logger for python3.
        ''',
        long_description_content_type="text/markdown",
        long_description=fd.read(),
        author="thepoy",
        author_email="thepoy@163.com",
        url="https://github.com/thep0y/python-logger",
        license="MIT",
        keywords="log logger logging colorful",
        packages=find_packages(),
        install_requires=[
            "colort",
        ],
    )
