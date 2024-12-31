#!/usr/bin/ python
# -*- coding: utf-8 -*-
# @Author  : ysl
# @File    : get_cookie.py
import json
import requests
from conf import *


class GetCookie:

    def __init__(self):
        pass

    def get_cookie(self, platform):
        data = {"url": platform}
        response = requests.post(get_cookie_api, json=data).json()
        cookies = json.loads(response['ck'])
        cookie = dict()
        for i in cookies:
            cookie[i['name']] = i['value']
        if platform == '新浪看点':
            temp_cookie = dict()
            if 'SUB' in cookie:
                temp_cookie['SUB'] = cookie['SUB']
                return temp_cookie
            else:
                return cookie
        else:
            return cookie


if __name__ == '__main__':
    cookies = GetCookie()
    print(cookies.get_cookie('dz:toutiaohao:cookie'))
