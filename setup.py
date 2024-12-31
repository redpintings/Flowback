#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : ysl
# @File    : setup.py
# @time    : 2024/6/17 14:30

from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess
from tqdm import tqdm
from typing import Mapping, Type
from distutils.cmd import Command


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
                    subprocess.check_call([self.executable, "-m", "pip", "install", req])
                except subprocess.CalledProcessError as e:
                    print(f"Failed to install {req}: {e}")
                    raise


setup(
    name='backflow',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
        'requests',
        'httpx',
        'tqdm',
        'chardet',
        'tldextract',
        'watchdog'
        # Add other dependencies as needed
    ],
    entry_points={
        'console_scripts': [
            'backflow=backflow.runner:main',
        ],
    },
    cmdclass={
        'install': CustomInstallCommand,
    }  # type: Mapping[str, Type[Command]]
)
