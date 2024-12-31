from celery import Celery
import importlib
import aiohttp
import asyncio
from conf import save_url
from utils.es_coon import EsConn
from typing import Dict, Union
from loguru import logger
from utils.save_com import Com
from utils.celery_app import app
# from utils.ding import *
from backflow.runner import SpiderRunner
from tenacity import retry, stop_after_attempt, wait_exponential


class Task:
    """
    Write the demo saved through Pipline according to your data storage needs, no matter how you want to write it
    """
    def __init__(self):
        self.headers: Dict[str, Union[str, int]] = {
            "Content-Type": 'application/json',
            "client-type": "3",
        }
        self.es_search = EsConn()
        self.com = Com()
        self.sem = asyncio.Semaphore(10)  # Initialize semaphore here

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def send_msg(self, msg: Dict[str, Union[str, int]]) -> None:
        if msg:
            title = msg.get('title')
            source_name = msg.get('source_name')
            item_ids = msg.get('es_ids', [])
            if not item_ids:
                item_ids = self.es_search.search_by_title(title) or []
            if title and item_ids:
                logger.warning(f'#@# title: {title} items_id: {item_ids} ')
                async with aiohttp.ClientSession() as session:
                    for item_id in item_ids:
                        form_data = {
                            "newsId": item_id,
                            "newsType": "NEWS",
                            "clickTimes": msg.get('pv', 0),
                            "likeTimes": msg.get('likes', 0),
                            "forwardingTimes": 0,
                            "collectTimes": 0,
                            "expTimes": 0,
                            "traExtTypeEnum": msg.get('traExtTypeEnum')
                        }
                        async with self.sem, session.post(save_url, json=form_data, headers=self.headers,
                                                          timeout=20) as response:
                            try:
                                resp = await response.json()
                            except aiohttp.ContentTypeError:
                                resp = await response.text()
                            except Exception as e:
                                logger.error(f'Error parsing response: {e}')
                                continue

                            logger.warning(":**msg**:{}", msg)
                            logger.warning(":Data save response:{}", resp)
                            coms_ = msg.get('comments', {})
                            coms = coms_.get('comments', []) if coms_ else []
                            if coms:
                                logger.warning(f'评论保存开始: item_id: {item_id} comments: {coms}')
                                try:
                                    com_res = await self.com.save_com(coms, item_id)
                                    logger.warning(f'评论保存成功: item_id: {item_id} content: {com_res}')
                                except Exception as e:
                                    logger.error(f'评论保存失败: item_id: {item_id} error: {e}')
            else:
                logger.warning(f'{source_name}:Fun SendMsg: es news not found: {title}')



import traceback
import asyncio
import httpx
from celery import Celery
# from utils.ding import send_dingding


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
