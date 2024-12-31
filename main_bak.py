#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date  1/23
# @Author  : ysl
# @File    : main.py

import json
import sys
import os
import requests
import asyncio
import aiohttp
import importlib
from loguru import logger
from itertools import islice
from conf import *
from utils.es_coon import EsConn
from typing import List, Dict, Union, Optional
from utils.save_com import Com

logger.add("../log/back.log",
           rotation="500 MB",
           format="<c>{time:YYYY-MM-DD HH:mm:ss}</c> {level} {message}",
           level="INFO")


class BackProcessor:
    def __init__(self):
        self.headers: Dict[str, Union[str, int]] = {
            "Content-Type": 'application/json',
            "client-type": "3",
        }
        self.es_search = EsConn()
        self.com = Com()
        self.sem = asyncio.Semaphore(10)  # 控制并发任务数量

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
                                                          timeout=10) as response:
                            resp = await response.json()
                            logger.info(":gov-msg:{}", msg)
                            logger.info(":gov-res:{}", resp)
                            logger.warning(resp)
                            coms = msg.get('comments', {}).get('comments', [])
                            if coms:
                                try:
                                    com_res = await self.com.save_com(coms, item_id)
                                    logger.warning(f'评论保存成功: item_id: {item_id} content: {com_res}')
                                except Exception as e:
                                    logger.error(f'评论保存失败: item_id: {item_id} error: {e}')
            else:
                logger.warning(f'{source_name}:未找到相关新闻: {title}')

    @staticmethod
    async def py_name() -> List[str]:
        loop = asyncio.get_running_loop()
        names = await loop.run_in_executor(None, os.listdir, paths)
        py_names = [name.replace('.py', '') for name in names if name.endswith(".py") and "dz_" in name]
        return py_names

    @staticmethod
    async def convert_to_camel_case(word: str) -> str:
        parts = word.split('_')
        camel_case_word = ''.join(part.capitalize() for part in parts)
        return camel_case_word

    async def process(self, module_name: str) -> None:
        try:
            module_path = f"spiders.{module_name}"
            module = importlib.import_module(module_path)
            cls_name = await self.convert_to_camel_case(module_name)
            cls = getattr(module, cls_name)
            instance = cls()
            start_method = getattr(instance, 'start', None)
            if start_method:
                for info in start_method():
                    try:
                        if not info:
                            continue
                        await self.send_msg(info)
                    except Exception as e:
                        logger.error(f"Failed to send message for module {module_name}: {str(e)}")
        except ImportError as ie:
            logger.warning(f"Failed to import module {module_name}: {str(ie)}")

    async def main(self) -> None:
        tasks = []
        module_names = await self.py_name()
        for module_name in module_names:
            task = asyncio.ensure_future(self.process(module_name))
            tasks.append(task)
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    processor = BackProcessor()
    loop.run_until_complete(processor.main())
