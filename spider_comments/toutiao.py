#!/usr/bin/ python
# -*- coding: utf-8 -*-
# @Author  : ysl
# @Time    : 2024/02/01 16:00:00
# @File    : toutiao.py
from utils.tools import Tools
from utils.get_cookie import GetCookie
import requests
import time
import json


class SpiderTt(object):
    """
    The demo collected from the comments of Today's Headlines is for reference only
    今日头条的评论采集的demo 仅作参考
    """

    def __init__(self):
        self.ck = 'xxx'

    def tt_comment(self, option):
        """
        今日头条评论获取
        """
        item_id = option.get('source_news_id')
        read_count = option.get('pv')
        comment_count = option.get('comment_count')
        items = []
        url = ("https://mp.toutiao.com/mp/agw/comment/article_comment_list?offset={}&count=20&"
               "item_id={}&group_id={}&sort=time&app_id=1231")
        var_headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
        for offset in range(0, comment_count, 20):
            comments_list = None
            time.sleep(1)
            try:
                comments_list = self.send_req(url.format(offset, item_id, item_id), var_headers)
            except Exception as e:
                print(e)
            print(offset, '+++')
            if not comments_list:
                break
            for comment in comments_list.get('data'):
                content = comment.get('content')
                try:
                    _content = Tools().parse_emoji(content.replace('\n', ''))
                except Exception as e:
                    print(e)
                    _content = content
                user = comment.get('user')
                user_avatar = user.get('avatar_url')
                user_name = user.get('screen_name')
                item = {
                    "content": _content,
                    "user_avatar": user_avatar,
                    "source": '头条',
                    "user_name": user_name,
                    "source_news_id": item_id,
                }
                if content and len(content) > 0:
                    items.append(item)
        return {"pv": int(read_count), "comments": items}

    def send_req(self, url, head):
        resp = requests.get(url, headers=head, verify=False, timeout=30, cookies=self.ck).text
        ret_data = json.loads(resp)
        comments_list = ret_data.get('data')
        return comments_list


if __name__ == '__main__':
    c = SpiderTt()
    dt = c.tt_comment({'item_id': '7328268615734985225', 'source_news_id': '7328268615734985225',
                       'name': 'jinritoutiao', "comment_count": 40,
                       "pv": 58968})
    print(dt)