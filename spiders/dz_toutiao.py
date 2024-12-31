#!/usr/bin/ python
# -*- coding: utf-8 -*-
# @Author  : ysl
# @File    : toutiao.py

import requests
import traceback
from loguru import logger
from utils.get_cookie import GetCookie
from utils.tools import Tools
from backflow.base import BackFlow
from backflow.middleware import Request
from spider_comments.toutiao import SpiderTt


class DzToutiao(BackFlow):
    """
    Today's headline data demo is for reference only
    """
    name = 'jinritoutiao'

    def __init__(self):
        super().__init__()
        self.ck = GetCookie().get_cookie('dz:toutiaohao:cookie')
        self.headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like "
                          "Gecko) Chrome/108.0.0.0 Safari/537.36"
        }

    async def get_page_request(self, page):
        url = (
            'https://mp.toutiao.com/api/feed/mp_provider/v1/?provider_type=mp_provider&aid=13'
            '&app_name=news_article&category=mp_all&channel=&stream_api_version=88&genre_typ'
            'e_switch=%7B%22repost%22%3A1%2C%22small_video%22%3A1%2C%22toutiao_graphic%22%3A'
            '1%2C%22weitoutiao%22%3A1%2C%22xigua_video%22%3A1%7D&device_platform=pc&platform'
            '_id=0&visited_uid=3340580883&offset={}&count=10&keyword=&client_extra_params=%7B'
            '%22category%22%3A%22mp_all%22%2C%22real_app_id%22%3A%221231%22%2C%22need_forwar'
            'd%22%3A%22true%22%2C%22offset_mode%22%3A%221%22%2C%22page_index%22%3A%226%22%2C%'
            '22status%22%3A%228%22%2C%22source%22%3A%220%22%7D&app_id=1231'
        ).format(page)
        yield Request('GET', url=url, headers=self.headers, cookies=self.ck, meta={'page': page})

    async def parse(self, response):
        try:
            resp = response.json()
            datas = resp.get('data', {})
            if not datas:
                print('toutiao cookie might be expired or no data returned.')
                return

            for con in datas:
                item, pv = dict(), 0
                assembleCell = con.get('assembleCell')
                itemCell = assembleCell.get('itemCell')
                articleBase = itemCell.get('articleBase')
                itemCounter = itemCell.get('itemCounter')

                item_id = articleBase.get('groupID')
                comment_count = itemCounter.get('commentCount')
                likes = itemCounter.get('diggCount')  # 点赞/喜欢
                impression_count = itemCounter.get('showCount')  # 推荐量
                item_type = 'all'
                title = articleBase.get('title')
                publish_time = articleBase.get('publishTime')
                readCount = itemCounter.get('readCount', 0)
                videoWatchCount = itemCounter.get('videoWatchCount', 0)
                pv = readCount or videoWatchCount

                org_url = "https://www.toutiao.com/i%s/" % item_id
                pv = int(pv)
                news = {
                    "tags": [],
                    "item_type": item_type,
                    "traExtTypeEnum": 'TOUTIAO',
                    "publish_time": Tools.date_transform(publish_time),
                    "from_source": self.name,
                    "source_name": '头条',
                    'url': org_url,
                    "original_link": org_url,
                    "original": '',
                    "img": [],
                    "source_news_id": item_id,
                    "comment_count": comment_count,  # 评论量
                    "title": title,
                    "company_name": '大众',
                    "author_flag": 0,
                    "pv": pv,
                    "hash_id": Tools.md5_hash("%s%s" % (self.name, item_id)),
                    "expose": impression_count,  # 推荐量
                    "reading_progress": None,  # 阅读进度
                    "share": 0,  # 分享
                    "likes": likes,  # 点赞/喜欢
                    "collection": 0,  # 收藏
                }
                if int(comment_count) > 0:
                    res_comments = SpiderTt().tt_comment(news)
                    if isinstance(res_comments, dict):
                        news['comments'] = res_comments
                yield news
        except Exception as e:
            logger.error(f"An error occurred while parsing the response: {e}")
            traceback.print_exc()

