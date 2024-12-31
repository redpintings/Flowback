#!/usr/bin/ python
# -*- coding: utf-8 -*-
# @Author  : ysl
# @File    : main.py
# @Time    : 2024/7/2 16:20

import json
import requests
from cookie_father import load
from http.cookiejar import CookieJar
from loguru import logger


class CK:
    def __init__(self):
        self.url = "http://dzainews.dzplus.dzng.com/save_cookie"

    @staticmethod
    def translate(c: CookieJar):
        return requests.utils.dict_from_cookiejar(c)

    def get(self, data):
        """Get cookie."""
        resp = self.request(data)
        if resp:
            cj = json.loads(resp.get('cookie'))
            return cj
        return None

    def load(self, domain_name_lst):
        cookies = load(domain_name=domain_name_lst)
        for key, v in cookies.items():
            dict_ck = self.translate(v)
            yield key, dict_ck

    def save(self, key, dict_ck):
        response = self.request({"name": key, "cookie": json.dumps(dict_ck)}, method='post')
        if response:
            logger.info(f"Cookie for {key} saved successfully.")
        else:
            logger.error(f"Failed to save cookie for {key}.")

    def request(self, data, method=None):
        try:
            if method == 'post':
                response = requests.post(self.url, json=data)
            else:
                response = requests.get(self.url, params=data)

            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Request failed with status code {response.status_code}")
        except requests.RequestException as e:
            logger.error(f"Request exception: {e}")
        return None


if __name__ == '__main__':
    domain_name_lst = ['163.com', 'yidianzixun.com', 'baidu.com', 'pdnews.cn', 'toutiao.com', 'sina.com.cn']
    cks = CK()
    cookies_dict = {}
    for key, ck in cks.load(domain_name_lst):
        logger.info(f"Loaded cookie for domain: {key}")
        cookies_dict[key] = ck
        print(key, ck)
        cks.save(key, ck)
    logger.info(f"Cookies loaded: {cookies_dict.keys()}")
