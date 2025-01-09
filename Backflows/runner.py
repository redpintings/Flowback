#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : ysl
# @File    : runner.py
import os
import sys
import time
import importlib
import inspect
import argparse
import traceback
import requests
import httpx
import asyncio
import importlib.util
import inspect
from loguru import logger

PROJECT_CONTEXT = False  # 初始化 PROJECT_CONTEXT

# 过滤掉不需要检查的目录
EXCLUDED_DIRS = {'venv', '__pycache__', 'build', 'dist'}


# 递归向下检查是否存在 settings.py
def find_settings_file(base_dir, max_depth=2, current_depth=0):
    if current_depth > max_depth:  # 超过最大深度则停止
        return None

    # 检查当前目录
    for file in os.listdir(base_dir):
        file_path = os.path.join(base_dir, file)
        if file == 'settings.py' and os.path.isfile(file_path):
            return file_path

    # 递归检查子目录
    for dir_name in os.listdir(base_dir):
        dir_path = os.path.join(base_dir, dir_name)
        if os.path.isdir(dir_path) and dir_name not in EXCLUDED_DIRS:
            found = find_settings_file(dir_path, max_depth, current_depth + 1)
            if found:
                return found

    return None


# 获取项目上下文
def is_project_context():
    current_dir = os.getcwd()
    settings_path = find_settings_file(current_dir)
    if settings_path:
        # 将包含 settings.py 的目录添加到 sys.path
        sys.path.insert(0, os.path.dirname(settings_path))
        return settings_path
    return None


# 主逻辑
settings_path = is_project_context()
if settings_path:
    # settings.py 所在目录
    settings_dir = os.path.dirname(settings_path)
    # spiders 目录路径应基于 settings.py 所在目录
    spider_dir = os.path.join(settings_dir, 'spiders')
    # print('settings_path:', settings_path)
    # print('spider_dir:', spider_dir)
else:
    print('settings.py 未找到，无法确定项目上下文')
# If in a project context, add the current directory to sys.path
if is_project_context():
    sys.path.insert(0, os.getcwd())
    PROJECT_CONTEXT = True
    try:
        import settings
        from downloadMiddleware import UserAgentMiddleware, RetryMiddleware, ProxyMiddleware
        from pipeline import Pipeline

        # logger.info("Running in project context.")
    except ImportError as e:
        logger.error(f"Error importing project modules: {e}")
        sys.exit(1)  # Exit if essential project modules are missing
else:
    try:
        from backflow_core import settings
        from backflow_core.downloadMiddleware import UserAgentMiddleware, RetryMiddleware, ProxyMiddleware
        from backflow_core.pipeline import Pipeline

        logger.info("Running outside project context, using installed package.")
    except ImportError as e:
        logger.error(f"Error importing backflow_core modules: {e}")
        sys.exit(1)

from Backflows.middleware import MiddlewareManager
from Backflows.template_project import create_project_structure
from Backflows.base import BackFlow


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
        # Check for spiders in the project's 'spiders' directory first
        if PROJECT_CONTEXT:
            # 遍历目录下的所有文件
            for filename in os.listdir(spider_dir):
                # 只处理 .py 文件，且排除 __init__.py
                if filename.endswith('.py') and filename != '__init__.py':
                    module_name = filename[:-3]  # 去掉 .py 后缀
                    module_path = os.path.join(spider_dir, filename)

                    # 动态加载模块
                    spec = importlib.util.spec_from_file_location(module_name, module_path)
                    if spec is None:
                        continue  # 如果无法加载模块，跳过
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)

                    # 查找符合条件的类
                    for name, obj in inspect.getmembers(mod):
                        if inspect.isclass(obj) and issubclass(obj, BackFlow) and obj is not BackFlow:
                            spiders[obj.name] = obj

        # If not in project context or no spiders found in the project, check installed package
        if not PROJECT_CONTEXT:
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
                async with httpx.AsyncClient(proxy=proxy, timeout=30) as client:  # 增加连接超时时间为 30 秒
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
                    pipeline = Pipeline()  # Use the dynamically imported Pipeline
                    await pipeline.process_item(item)  # Use await here
                spider.increment_pages_crawled()  # Increment pages crawled
                self.pages_crawled += 1

    async def run(self, name, distributed=False, stop=settings.END_PAGE, step=settings.PAGE_STEP):
        self.start_time = time.time()
        if distributed:
            # Assuming tasks.py is in the backflow_core when installed, and in the project root when running a project
            if PROJECT_CONTEXT:
                try:
                    from tasks import run_spider
                except ImportError:
                    from backflow_core.tasks import run_spider
            else:
                from backflow_core.tasks import run_spider
            for page in range(settings.START_PAGE, stop, step):
                run_spider.delay(name, page)
        else:
            self.print_stats()
            tasks = [self.run_single_page(name, page) for page in range(settings.START_PAGE, stop, step)]
            await asyncio.gather(*tasks)
        self.end_time = time.time()  # Set end_time here, regardless of distributed mode
        self.print_stats()

    def print_stats(self):
        if self.end_time is not None and self.start_time is not None:
            total_time = self.end_time - self.start_time
            print(f"Spider run completed.")
            print(f"Total pages crawled: {self.pages_crawled}")
            print(f"Total requests sent: {self.requests_sent}")
            print(f"Total run time: {total_time:.2f} seconds")
        else:
            print("Spider run completed. Timing information not available.")


def create_spider_file(spider_name):
    from Backflows.template import template
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

    new_project_parser = subparsers.add_parser("new", help="Add a new project")
    new_project_parser.add_argument("project_name", default='NewSpiders',
                                    help="The name of the new spider project to add")

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
        print(f"Project '{args.project_name}' created. Please navigate into the project directory to run spiders.")
    else:
        parser.print_help()


if __name__ == "__main__":
    s = SpiderRunner()
    s.find_spiders()
