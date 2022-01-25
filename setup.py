#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import setuptools


package_dir = {"": "./src/plugins"}

packages = [
    "nonebot-general-rss",
    "nonebot-general-rss.RSS",
    "nonebot-general-rss.RSS.routes",
    "nonebot-general-rss.RSS.routes.Parsing",
]

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
    package_dir=package_dir,
    packages=packages,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8.3,<3.10.0",
    install_requires=[
        "nb-cli>=0.6.4,<0.7.0",
        "nonebot2==2.0.0b1",
        "nonebot-adapter-onebot==2.0.0b1",
        "nonebot-plugin-apscheduler>=0.1.2,<0.2.0",
        "feedparser>=6.0.0,<6.1.0",
        "pyquery>=1.4.3,<1.5.0",
        "aiofiles>=0.5.0,<0.6.0",
        "emoji>=0.5.4,<0.6.0",
        "google-trans-new>=1.1.9,<1.2.0",
        "Pillow>=8.1.1",
        "typing-extensions>=3.10.0.2,<3.11.0.0",
        "python-qbittorrent>=0.4.2,<0.5.0",
        "magneturi>=1.3,<2.0",
        "ImageHash>=4.2.0,<4.3.0",
        "tenacity>=7.0.0,<7.1.0",
        "bbcode>=1.1.0,<1.2.0",
        "tinydb>=4.5.1,<4.6.0",
    ],
)
