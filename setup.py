#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : ysl
# @File    : setup.py
# @time    : 2024/6/17 14:30

from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess
from tqdm import tqdm
import sys  # Import the sys module

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


class CustomInstallCommand(install):
    """Customized setuptools install command to display a progress bar."""

    def run(self):
        # Run the standard install process
        install.run(self)

        # Display a progress bar for the installation of dependencies
        requirements = self.distribution.install_requires
        if requirements:
            for req in tqdm(requirements, desc="Installing dependencies"):
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", req])
                except subprocess.CalledProcessError as e:
                    print(f"Failed to install {req}: {e}")
                    raise


setup(
    name='backflow',
    version='0.1.3',
    author='ysl',  # 替换为你的名字
    author_email='runfastpluszz@gmail.com',  # 替换为你的邮箱
    description='A simple crawler framework that implements both single run and distributed run based on Celery,'
                ' allowing you to write your crawler code as you please',  # 替换为你的项目简短描述
    long_description=long_description,
    long_description_content_type="text/markdown",  # 如果你的 README 是 Markdown
    url='https://github.com/redpintings/Flowback',  # 替换为你的项目 GitHub 仓库地址
    license='MIT',  # 替换为你的开源协议
    packages=find_packages(),
    install_requires=[
        'aiohttp==3.10.11',
        'celery==5.2.7',
        'elasticsearch==7.17.3',
        'loguru',
        'PyExecJS',
        'requests',
        'pymongo',
        'argparse',
        'tqdm',
        'httpx',
        'Js2Py',
        'watchdog',
        'tldextract',
        'lxml',
        'beautifulsoup4',
        'pytz',
        'chardet',
        'tenacity',
    ],
    entry_points={
        'console_scripts': [
            'backflow=backflow.runner:main',
        ],
    },
    cmdclass={
        'install': CustomInstallCommand,
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # 替换为你的开源协议
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # 指定支持的 Python 版本
)
