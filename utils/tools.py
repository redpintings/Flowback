#!/usr/bin/ python
# -*- coding: utf-8 -*-
# @Author  : ysl
# @File    : tools.py


from loguru import logger
from datetime import datetime
from emojis.emoji import Emoji
import hashlib
import datetime
import requests
import json
import time
from html import unescape
import re


class Tools(object):
    def __init__(self):
        self.emj = Emoji()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, '
                          'like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Content-Type': 'application/json'
        }

    def parse_emoji(self, msg):
        return self.emj.parse_emoji(msg)

    @staticmethod
    def md5_hash(data):
        hash_id = hashlib.md5(data.encode(encoding='UTF-8')).hexdigest()
        return hash_id

    @staticmethod
    def _md5(name, _id):
        """
        数据回流使用
        :param name:
        :param _id:
        :return:
        """
        xdd = '%s-%s' % (name, _id)
        hash_id = hashlib.md5(xdd.encode(encoding='UTF-8')).hexdigest()
        return hash_id

    @staticmethod
    def local_time():
        # 获取当前时间
        now = datetime.now()
        # 格式化时间
        formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
        return formatted_time

    @staticmethod
    def date_transform(time_stamp):
        """
        时间戳转换工具
        :param time_stamp:
        :return:
        """
        if not time_stamp:
            return Tools.local_time()
        time_array = time.localtime(time_stamp)
        other_style_time = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
        return other_style_time


class UauTool(object):
    headers = {
        "tout_app": "News 7.7.5 rv:7.7.5.16 (iPhone; iOS 13.4.1; zh_CN) Cronet",
        "tout_pc": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/78.0.3904.108 Safari/537.36",
        "wb_app": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 "
                  "(KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
        "tout_live": "com.ss.android.article.news/7570 (Linux; U; Android 5.1.1; zh_CN; vivo X7; "
                     "Build/LMY47V; Cronet/TTNetVersion:3e14bd94 2019-12-05)",
        'wy': "NewsApp/23.0 iOS/11.1.1 (iPhone8,1)",
        'Firefox': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.8) Gecko/20100101 Firefox/60.8'
    }