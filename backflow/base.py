#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : ysl
# @File    : base.py
# @Time    : 2024/6/16 16:02

import logging
import os
import signal
import sys
import re
import chardet
import urllib3
import requests
import tldextract
from bs4 import BeautifulSoup
from lxml import html
# from loguru import logger
from urllib.parse import urlparse, urljoin
from utils.es_coon import EsConn
from logging.handlers import RotatingFileHandler
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from concurrent.futures import ThreadPoolExecutor

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Module-level logger
logger = logging.getLogger('backflow_logger')
logger.setLevel(logging.INFO)

# Ensure logger is only configured once
if not logger.hasHandlers():
    log_dir = os.path.join(os.path.dirname(os.getcwd()), 'log')
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'execution_log.log')

    # Use RotatingFileHandler to limit log file size and number of backup files
    handler = RotatingFileHandler(log_file, maxBytes=20 * 1024 * 1024, backupCount=3)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def signal_handler(signum, frame):
    sys.exit(0)


class BackFlow:
    name = None

    def __init__(self):
        self.logger = logger

        # Set up signal handlers
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)

        # Initialize statistics
        self.pages_crawled = 0
        self.requests_sent = 0

    def increment_pages_crawled(self):
        self.pages_crawled += 1

    def increment_requests_sent(self):
        self.requests_sent += 1

    def get_page_request(self, page):
        """
        Get the request object for the specified page.
        This method should be implemented by all subclasses.
        """
        raise NotImplementedError(f'{self.__class__.__name__}.get_page_request function is not defined')

    def parse(self, response):
        """
        Parse the response object and yield items.
        This method should be implemented by all subclasses.
        """
        raise NotImplementedError(f'{self.__class__.__name__}.parse function is not defined')

    def __str__(self):
        """
        String representation of the instance.
        """
        return f"<{type(self).__name__} {self.name!r} at 0x{id(self):0x}>"

    __repr__ = __str__


