#!/usr/bin/ python
# -*- coding: utf-8 -*-
# @Author  : ysl
# @File    : celery_app.py

from celery import Celery
from conf import CeleryConf

name = CeleryConf.REDIS_NAME
host = CeleryConf.REDIS_HOST
port = CeleryConf.REDIS_POST
db = CeleryConf.REDIS_DB_BROKER
db_res = CeleryConf.REDIS_DB_RESULT
pwd = CeleryConf.REDIS_PWD

# Including the password in the connection string
app_save_conf = '{celery_type}://:{pwd}@{host}:{port}/{db}'.format(
    celery_type=name,
    pwd=pwd,
    host=host,
    port=port,
    db=db
)

app = Celery(broker=app_save_conf)
app.conf.broker_url = app_save_conf
app.conf.result_backend = '{celery_type}://:{pwd}@{host}:{port}/{db_res}'.format(
    celery_type=name,
    pwd=pwd,
    host=host,
    port=port,
    db_res=db_res
)

# python3 -m celery -A scheduler worker -c 2 -P gevent --loglevel=debug
