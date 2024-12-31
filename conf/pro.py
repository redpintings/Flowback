#!/usr/bin/ python
# -*- coding: utf-8 -*-
# @Author  : ysl
# @File    : pro.py

class Es:
    host = "xxx"
    port = 9200
    username = "xx"
    password = "xxx"


class CeleryConf(object):
    REDIS_NAME = 'redis'
    REDIS_HOST = "xx"
    REDIS_POST = 6379
    REDIS_DB_BROKER = 10
    REDIS_DB_RESULT = 11
    REDIS_PWD = 'xxx'


class Page(object):
    normal = 200
    abnormal = 1600
    startPage = 0


# api
get_cookie_api = ""
paths = "/opt/workstation/dz_data_back/spiders"
save_url = ""
# TODO 添加正式服的url

save_com = ''

celery_path = "/opt/workstation/dz_data_back"
