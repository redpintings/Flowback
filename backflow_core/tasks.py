import importlib
import aiohttp
import asyncio
# from typing import Dict, Union
# from loguru import logger
from utils.celery_app import app
from Backflows.runner import SpiderRunner
# from tenacity import retry, stop_after_attempt, wait_exponential
import traceback
import asyncio
# import httpx
# from celery import Celery


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
            # await send_dingding(f'An error occurred while running spider@xx: \n {trace}')

    asyncio.run(async_run_spider())
