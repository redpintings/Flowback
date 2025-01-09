# -*- coding: utf-8 -*-
# @Author  : ysl
# @File    : dongfangcaifu.py.py

from loguru import logger
from utils.tools import Tools
from Backflows.base import BackFlow
from Backflows.middleware import Request
from parsel import Selector
import traceback


class Dongfangcaifu(BackFlow):
    name = 'dongfangcaifu'

    def __init__(self):
        super().__init__()
        self.ck = None
        self.headers = {
            'Cookie': 'st_si=07577822841164; st_asi=delete; qgqp_b_id=29bf1bcc2d53a8587adedc785cc087ba; st_pvi=23828108194402; st_sp=2024-12-03%2014%3A12%3A08; st_inirUrl=https%3A%2F%2Fwww.google.com%2F; st_sn=162; st_psi=20250106105653308-113104302701-4707866973',
            'Referer': 'https://finance.eastmoney.com/a/ccjdd_2.html',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        }

    async def get_page_request(self, page):
        url = 'https://finance.eastmoney.com/a/ccjdd_{}.html'.format(page)
        yield Request('GET', url=url, headers=self.headers, cookies=self.ck, meta={'page': page})

    async def parse(self, response):
        resp = response.text
        resp = Selector(resp)
        nodes = resp.xpath("//div[@class='artitleList']//li//a")
        for node in nodes:
            title = node.xpath("./text()").get()
            url = node.xpath("./@href").get()
            news = {
                'url': url,
                'title': title,
            }
            yield news
