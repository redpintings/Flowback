#!/usr/bin/ python
# -*- coding: utf-8 -*-
# @Author  : ysl
# @File    : template.py


def template(spider_name):
    spider_template = f"""
from loguru import logger
from utils.get_cookie import GetCookie
from utils.tools import Tools
from backflow.base import BackFlow
from backflow.middleware import Request
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

    def get_page_request(self, page):
        url = 'http://example.com/api/data?page={{}}'.format(page)
        yield Request('GET', url=url, headers=self.headers, cookies=self.ck, meta={{'page': page}})

    async def parse(self, response):
        try:
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
        except Exception as e:
            logger.error(f"An error occurred while parsing the response: {{e}}")
            traceback.print_exc()
        """
    return spider_template
