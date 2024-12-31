#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : ysl
# @File    : dz_yidianhao.py

import sys
import aiohttp
import requests
import traceback
from loguru import logger
from urllib.parse import unquote
from utils.get_cookie import GetCookie
from utils.tools import Tools
from backflow.base import BackFlow
from js_token.run import Token
from backflow.middleware import Request


class DzYidianhao(BackFlow):
    """
    一点资讯 图文
    """
    name = 'yidianzixun'

    def __init__(self):
        super().__init__()
        self.ck = GetCookie().get_cookie("dz:yidianhao:cookie")
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh,zh-HK;q=0.9,zh-CN;q=0.8',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://mp.yidianzixun.com/',
            'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not.A.Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'x-mp-code': '865f32e715083c9e9ded3c95d6d65e4d',
        }

    def get_id(self, _id=0):
        url = "https://mp.yidianzixun.com/api/get-Article-id?id={}".format(_id)
        res = requests.get(url, headers=self.headers, cookies=self.ck)
        return res.json().get('result')

    async def get_page_request(self, page):
        id_ = self.get_id(page)
        article_token = Token().yidian(id_)
        url = (
            "https://mp.yidianzixun.com/model/Article?token={}&page={}&page_size=10&status=2,6,7"
            "&has_data=1&type=all&article_type=&push_status=&date=&title=".format(article_token, page)
        )
        yield Request('GET', url=url, headers=self.headers, cookies=self.ck, meta={'page': page, "xx": 123})

    async def parse(self, response):
        try:
            logger.warning(f"Parsing****xxxxxxxx {response.meta}")
            resp = response.json()
            data = resp.get('posts', {})
            if not data:
                print('yidianzixun cookie might be expired or no data returned.')
                return

            for con in data:
                all_data = con.get('all_data')
                title = con.get('title')
                publish_time = con.get('date')
                item_id = con.get('newsId')
                pv = all_data.get('clickDoc')
                pv = int(pv) if pv else 0
                reco_count = all_data.get('viewDoc')
                com_count = all_data.get('addCommentDoc')
                url = "https://www.yidianzixun.com/article/{}".format(item_id)
                news = {
                    "tags": [],
                    "item_type": "article",
                    "traExtTypeEnum": 'YIDIANZIXUN',
                    "publish_time": publish_time,
                    "from_source": self.name,
                    "source_name": '一点资讯',
                    'url': url,
                    "original_link": url,
                    "original": '',
                    "img": [],
                    "source_news_id": item_id,
                    "comment_count": com_count,  # 评论量
                    "title": title,
                    "company_name": '大众',
                    "author_flag": 0,
                    "pv": pv,
                    "hash_id": Tools.md5_hash("%s%s" % (self.name, item_id)),
                    "expose": reco_count,  # 推荐量
                    "reading_progress": None,  # 阅读进度
                    "share": 0,  # 分享
                    "collection": 0,  # 收藏
                }
                yield news
        except Exception as e:
            logger.error(f"An error occurred while parsing the response: {e}")
            traceback.print_exc()