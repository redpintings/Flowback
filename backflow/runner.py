#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : ysl
# @File    : runner.py
# @Software: PyCharm
import os
import sys
import time
import importlib
import inspect
import argparse
import traceback
import requests
# from conf import Page
import settings
import httpx
import asyncio
# from utils.ding import DingDingSender
from backflow.base import BackFlow
from loguru import logger
from downloadMiddleware import UserAgentMiddleware, RetryMiddleware, ProxyMiddleware
from .middleware import MiddlewareManager


class UpperAttrMetaclass(type):
    _type_registry = {}

    def __new__(cls, cls_name, bases, attr_dict):
        new_cls = super().__new__(cls, cls_name, bases, attr_dict)

        # Register the class with its 'name' attribute
        if 'name' in attr_dict:
            cls._type_registry[attr_dict['name']] = new_cls

        return new_cls

    @classmethod
    def get_type(cls, name):
        return cls._type_registry.get(name)

    @classmethod
    def list_registered_types(cls):
        return list(cls._type_registry.keys())

    @classmethod
    def unregister_type(cls, name):
        if name in cls._type_registry:
            del cls._type_registry[name]


class SpiderRunner:
    def __init__(self):
        self.spider_modules = ['spiders']
        self.middlewares = self.load_middlewares()
        self.pages_crawled = 0
        self.requests_sent = 0
        self.start_time = None
        self.end_time = None
        self.semaphore = asyncio.Semaphore(settings.MAX_CONCURRENT_REQUESTS)  # 限制并发请求数量

    def load_middlewares(self):
        middleware_classes = {
            'UserAgentMiddleware': UserAgentMiddleware,
            'RetryMiddleware': RetryMiddleware,
            'ProxyMiddleware': ProxyMiddleware,
        }

        middlewares = []
        for middleware_name in settings.MIDDLEWARES:
            middleware_class = middleware_classes.get(middleware_name)
            if middleware_class:
                middlewares.append(middleware_class())
        return MiddlewareManager(middlewares)

    def find_spiders(self):
        spiders = {}
        for module in self.spider_modules:
            mod = importlib.import_module(module)
            for name, obj in inspect.getmembers(mod):
                if inspect.isclass(obj) and issubclass(obj, BackFlow) and obj is not BackFlow:
                    spiders[obj.name] = obj
        return spiders

    async def process_request(self, request):
        self.requests_sent += 1
        return await self.middlewares.process_request(request)

    async def process_response(self, request, response):
        return await self.middlewares.process_response(request, response)

    async def fetch_page(self, request):
        """
        httpx.AsyncClient 的 proxies 参数允许你为所有的请求设置一个默认的代理。
        这意味着当你使用这个 client 对象发送请求时，所有的请求都会通过指定的代理服务器发送
        """
        async with self.semaphore:  # 使用信号量限制并发请求数量
            request = await self.process_request(request)
            proxy = request.meta.get('proxy')
            try:
                async with httpx.AsyncClient(proxies=proxy, timeout=30) as client:  # 增加连接超时时间为 30 秒
                    if request.method == 'GET':
                        response = await client.get(request.url, headers=request.headers, cookies=request.cookies,
                                                    params=request.params)
                    elif request.method == 'POST':
                        response = await client.post(request.url, headers=request.headers, data=request.data,
                                                     cookies=request.cookies)

                response.meta = request.meta  # Attach meta information to the response
                response = await self.process_response(request, response)
                return response
            except (httpx.ConnectTimeout, httpx.ReadTimeout) as e:
                logger.error(f"Timeout error occurred: {e}")
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error occurred: {e}")
            except httpx.RequestError as e:
                logger.error(f"Request error occurred: {e}")
            except Exception as e:
                logger.error(f"An unexpected error occurred: {e}")
            return None

    async def run_single_page(self, name, page):
        spiders = self.find_spiders()
        spider_cls = spiders.get(name)
        if not spider_cls:
            raise ValueError(f"Spider with name '{name}' not found")

        spider = spider_cls()
        async for request in spider.get_page_request(page):
            spider.increment_requests_sent()  # Increment requests sent
            response = await self.fetch_page(request)
            if response is not None:
                async for item in spider.parse(response):
                    from pipeline import Pipeline
                    pipeline = Pipeline()
                    await pipeline.process_item(item)  # Use await here
                spider.increment_pages_crawled()  # Increment pages crawled
                self.pages_crawled += 1

    async def run(self, name, distributed=False, stop=settings.END_PAGE, step=settings.PAGE_STEP):
        self.start_time = time.time()
        if distributed:
            for page in range(settings.START_PAGE, stop, step):
                from tasks import run_spider
                run_spider.delay(name, page)
        else:
            self.check_settings()
            tasks = [self.run_single_page(name, page) for page in range(settings.START_PAGE, stop, step)]
            await asyncio.gather(*tasks)
            self.end_time = time.time()
            self.print_stats()

    def check_settings(self):
        try:
            import settings
            required_settings = ['MONGO_URI', 'MONGO_DATABASE', 'DATA_FILE_PATH', 'API_ENDPOINT',
                                 'START_PAGE', 'END_PAGE', 'PAGE_STEP']
            for setting in required_settings:
                if not hasattr(settings, setting):
                    raise ValueError(f"Missing required setting: {setting}")
        except ImportError:
            raise ImportError("settings.py file not found")

    def print_stats(self):
        total_time = self.end_time - self.start_time
        print(f"Spider run completed.")
        print(f"Total pages crawled: {self.pages_crawled}")
        print(f"Total requests sent: {self.requests_sent}")
        print(f"Total run time: {total_time:.2f} seconds")


def create_project_structure(project_name):
    """Create necessary directories and files for the project."""
    # Define project directories and files
    structure = [
        f"{project_name}",
        f"{project_name}/spiders",
        f"{project_name}/conf",
        f"{project_name}/conf/__init__.py",
        f"{project_name}/conf/local.py",
        f"{project_name}/settings.py",
        f"{project_name}/middlewares.py",
        f"{project_name}/pipelines.py",
        f"{project_name}/tasks.py",
    ]

    # Create directories and files
    for path in structure:
        if '.' in path:
            with open(path, 'w') as f:
                f.write("# This is an auto-generated file.\n")
        else:
            os.makedirs(path, exist_ok=True)
    print(f"Project '{project_name}' has been created successfully!")


def create_spider_file(spider_name):
    from .template import template
    spider_template = template(spider_name=spider_name)
    file_path = os.path.join('spiders', f'{spider_name}.py')
    with open(file_path, 'w') as f:
        f.write(spider_template)
    print(f"Spider file '{file_path}' created successfully.")


def main():
    parser = argparse.ArgumentParser(description="Backflow Spider Runner")
    subparsers = parser.add_subparsers(dest="command")

    crawl_parser = subparsers.add_parser("crawl", help="Crawl a spider")
    crawl_parser.add_argument("spider_name", help="The name of the spider to run")
    crawl_parser.add_argument("--distributed", action="store_true", help="Run the spider in distributed mode")
    crawl_parser.add_argument("--page", type=int, default=settings.END_PAGE,
                              help="The stop parameter for the range function")
    crawl_parser.add_argument("--step", type=int, default=1, help="The step parameter for the range function")

    list_parser = subparsers.add_parser("list", help="List all spiders")

    addspider_parser = subparsers.add_parser("addspider", help="Add a new spider")
    addspider_parser.add_argument("spider_name", default='newspider', help="The name of the new spider to add")

    addspider_parser = subparsers.add_parser("new", help="Add a new spider project")
    addspider_parser.add_argument("project_name", default='NewSpiders', help="The name of the new spider project to add")

    args = parser.parse_args()

    runner = SpiderRunner()

    if args.command == "crawl":
        asyncio.run(runner.run(args.spider_name, distributed=args.distributed, stop=args.page, step=args.step))
    elif args.command == "list":
        spiders = runner.find_spiders()
        print("Available spiders:")
        for spider_name in spiders.keys():
            print(f" - {spider_name}")
    elif args.command == "addspider":
        create_spider_file(args.spider_name)
    elif args.command == "new":
        create_project_structure(args.project_name)
    else:
        parser.print_help()


if __name__ == "__main__":
    s = SpiderRunner()
    s.find_spiders()
