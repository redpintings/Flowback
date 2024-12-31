#!/usr/bin/ python
# -*- coding: utf-8 -*-
# @Author  : ysl
# @File    : settings.py.py

# Configuration for the project

# MongoDB settings
MONGO_URI = 'mongodb://localhost:27017'
MONGO_DATABASE = 'spider_data'

# File settings
DATA_FILE_PATH = 'data/output.json'

# API settings
API_ENDPOINT = 'http://example.com/api/data'

# Other settings， 前提是你使用了 --page 参数
START_PAGE = 0  # The default starting page number to crawl
END_PAGE = 200  # The default ending page number to crawl
PAGE_STEP = 1  # The default step size to crawl the pages


MAX_RETRIES = 3  # The maximum number of retries for each request

# END_PAGE / PAGE_STEP = TotalNumber # total number of pages to crawl
# The MAX_CONCURRENT_REQUESTS parameter needs to be greater than the TotalNumber
MAX_CONCURRENT_REQUESTS = 300  # The maximum number of concurrent requests:
MIDDLEWARES = [
    'UserAgentMiddleware',
    'RetryMiddleware',
    # 'ProxyMiddleware',  # Uncomment to use
]

