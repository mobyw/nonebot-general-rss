#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r", encoding="UTF-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nonebot-general-rss",
    version="2.0.0",
    author="mobyw",
    author_email="mobyw66@gmail.com",
    description="基于ELF_RSS修改的支持频道的QQ机器人RSS订阅插件",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mobyw/nonebot-general-rss",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8,<=3.9",
)
