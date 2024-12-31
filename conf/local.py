#!/usr/bin/ python
# -*- coding: utf-8 -*-
# @Author  : ysl
# @File    : local.py


class Es:
    host = "xxx"
    port = 9200
    username = "xxx"
    password = "xxxx"


class CeleryConf(object):
    REDIS_NAME = 'redis'
    REDIS_HOST = "127.0.0.1"
    REDIS_POST = 6379
    REDIS_DB_BROKER = 10
    REDIS_DB_RESULT = 11
    REDIS_PWD = ''


# js
yidian_js = "/yidianzixun.js"
# api
get_cookie_api = "xxx"
paths = "/Users/ysl/Flowback/spiders"
save_url = ""
save_com = ''
celery_path = "/opt/workstation/dz_data_back"
