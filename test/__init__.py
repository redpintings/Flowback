# -*- coding: utf-8 -*-
# @Author  : ysl
# @File    : __init__.py.py
import requests
from parsel import Selector

url = 'https://finance.eastmoney.com/a/ccjdd_{}.html'.format(1)
headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like "
                          "Gecko) Chrome/108.0.0.0 Safari/537.36"
        }
resp = requests.get(url, headers=headers, verify=False).text
print(resp)
resp = Selector(resp)
nodes = resp.xpath("//div[@class='artitleList']//li//a/@href").getall()
print(nodes)