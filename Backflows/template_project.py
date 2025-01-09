#!/usr/bin/ python
# -*- coding: utf-8 -*-
# @Author  : ysl
# @File    : template_project.py
import os


def settings():
    set_template = """
#!/usr/bin/ python
# -*- coding: utf-8 -*-

# @File    : settings.py

# Configuration for the project

# MongoDB settings
MONGO_URI = 'mongodb://localhost:27017'
MONGO_DATABASE = 'spider_data'

# File settings
DATA_FILE_PATH = 'data/output.json'

# API settings
API_ENDPOINT = 'http://example.com/api/data'

# Other settings， 前提是你使用了 --page 参数
START_PAGE = 1  # The default starting page number to crawl
END_PAGE = 20  # The default ending page number to crawl
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
    """
    return set_template


def pipeline():
    pipeline_template = """
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : ysl
# @File    : pipeline.py

import os
import json
import pymongo
import asyncio
from settings import MONGO_URI, MONGO_DATABASE, DATA_FILE_PATH

class Pipeline:
    def __init__(self):
        # Initialize Task without creating Semaphore here
        pass

    async def process_item(self, item):
        # Process the item by storing it in a file, MongoDB, and an API endpoint.
        # Store item in file and MongoDB synchronously
        self.store_in_file(item)
        # self.store_in_mongo(item)

        # Store item in API asynchronously
        # await self.store_in_api(item)

    @staticmethod
    def store_in_file(item):
        # Store the item in a JSON file. If the file does not exist, create it.
        try:
            # Check if the directory exists, if not, create it
            directory = os.path.dirname(DATA_FILE_PATH)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)

            # Check if the file exists, if not, create it
            if not os.path.exists(DATA_FILE_PATH):
                with open(DATA_FILE_PATH, 'w') as f:
                    pass  # Just create an empty file

            # Append the item to the file
            with open(DATA_FILE_PATH, 'a') as f:
                json.dump(item, f)
                f.write('\\n')
        except Exception as e:
            print(f"Error storing item in file: {e}")

    @staticmethod
    def store_in_mongo(item):
        # Store the item in a MongoDB collection.
        try:
            client = pymongo.MongoClient(MONGO_URI)
            db = client[MONGO_DATABASE]
            collection = db['items']
            collection.insert_one(item)
        except Exception as e:
            print(f"Error storing item in MongoDB: {e}")

    async def store_in_api(self, item):
        # Send the item to an API endpoint.
        pass

    """
    return pipeline_template


def downloadMiddleware():
    dm_template = """
import random
from loguru import logger
import settings
# from backflow.middleware import DownloadMiddleware # Assuming this is in a relative path

class DownloadMiddleware: # Placeholder if backflow is not available
    async def process_request(self, request):
        return request

    async def process_response(self, request, response):
        return response

class UserAgentMiddleware(DownloadMiddleware):
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8',
        # Add more user agents
    ]

    async def process_request(self, request):
        user_agent = random.choice(self.USER_AGENTS)
        logger.warning(f'Using random user agent: {user_agent}')
        request.headers['User-Agent'] = user_agent
        return request

class RetryMiddleware(DownloadMiddleware):
    MAX_RETRIES = settings.MAX_RETRIES

    async def process_response(self, request, response):
        if response.status_code != 200 and request.meta.get('retry_times', 0) < self.MAX_RETRIES:
            retry_times = request.meta.get('retry_times', 0) + 1
            logger.warning(f"Retrying {request.url} (attempt {retry_times})")
            request.meta['retry_times'] = retry_times
            return await self.process_request(request)  # Retry the request
        return response

class ProxyMiddleware(DownloadMiddleware):
    PROXIES = [
        'http://proxy1.example.com:8000',
        'http://proxy2.example.com:8000',
        # Add more proxies
    ]

    async def process_request(self, request):
        proxy = random.choice(self.PROXIES)
        request.meta['proxy'] = proxy
        return request

    """
    return dm_template


def task():
    task_template = """
from celery import Celery
from loguru import logger
from utils.celery_app import app
from Backflows.runner import SpiderRunner
import traceback
import asyncio
import httpx
from celery import Celery

@app.task
def run_spider(name, page):
    async def async_run_spider():
        try:
            runner = SpiderRunner()
            await runner.run_single_page(name, page)
        except asyncio.TimeoutError:
            # 忽略 TimeoutError 异常
            print(f"Timeout occurred while running spider '{name}' for page {page}")
            return
        except Exception as e:
            print(f"An error occurred while running spider '{name}' for page {page}: {e}")
            traceback.print_exc()
            trace = traceback.format_exc()

    asyncio.run(async_run_spider())

    """
    return task_template


def conf():
    conf_template = """
#!/usr/bin/ python
# -*- coding: utf-8 -*-
# @File    : local.py

class CeleryConf(object):
    REDIS_NAME = 'redis'
    REDIS_HOST = "127.0.0.1"
    REDIS_POST = 6379
    REDIS_DB_BROKER = 10
    REDIS_DB_RESULT = 11
    REDIS_PWD = ''

paths = "/Users/ysl/Flowback/spiders"  # 你的当前的项目spiders路径
save_url = ""
save_com = ''
celery_path = "xxx" # 你的当前的项目路径
    """
    return conf_template


def conf_init():
    conf_init = """
from .local import *
"""
    return conf_init


def spider(spider_name):
    spider_template = f"""
from loguru import logger
from utils.tools import Tools
from Backflows.base import BackFlow
from Backflows.middleware import Request
import traceback

class {spider_name.capitalize()}(BackFlow):
    name = '{spider_name}'

    def __init__(self):
        super().__init__()
        self.ck = None
        self.headers = {{
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like "
                          "Gecko) Chrome/108.0.0.0 Safari/537.36"
        }}

    async def get_page_request(self, page):
        url = 'http://example.com/api/data?page={{}}'.format(page)
        yield Request('GET', url=url, headers=self.headers, cookies=self.ck, meta={{'page': page}})

    async def parse(self, response):
        resp = response.json()
        datas = resp.get('data', {{}})
        if not datas:
            print(f'{spider_name} cookie might be expired or no data returned.')
            return
        for con in datas:

            news = {{
                'url': con.get('item_id', ''),
            }}
            yield news
        """
    return spider_template


def create_project_structure(project_name):
    """Create necessary directories and files for the project."""
    # Define project directories and files in an order that ensures
    # directories are created before files within them.
    structure = [
        f"{project_name}",
        f"{project_name}/spiders",
        (f"{project_name}/spiders/new_spider.py", spider('newspider')),
        f"{project_name}/conf",
        (f"{project_name}/conf/__init__.py", conf_init()),
        (f"{project_name}/conf/local.py", conf()),
        (f"{project_name}/settings.py", settings()),
        (f"{project_name}/downloadMiddleware.py", downloadMiddleware()),
        (f"{project_name}/pipeline.py", pipeline()),
        (f"{project_name}/tasks.py", task()),
    ]

    # Create directories and files
    for item in structure:
        if isinstance(item, str):  # It's a directory
            if not os.path.exists(item):
                os.makedirs(item)
                print(f"Created directory: '{item}'")
            else:
                print(f"'{item}' already exists. Skipping creation.")
        elif isinstance(item, tuple):  # It's a file with content
            path, content_func = item
            dirname = os.path.dirname(path)
            if dirname and not os.path.exists(dirname):
                os.makedirs(dirname)
                print(f"Created directory: '{dirname}'")
            if not os.path.exists(path):
                with open(path, 'w') as f:
                    if content_func:
                        f.write(content_func)
                    else:
                        f.write("# This is an auto-generated file.\n")
                print(f"Created file: '{path}'")
            else:
                print(f"'{path}' already exists. Skipping creation.")

    print(f"Project '{project_name}' has been created successfully!")


if __name__ == '__main__':
    project_name = "my_crawler_project"
    create_project_structure(project_name)
