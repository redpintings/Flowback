#!/usr/bin/ python
# -*- coding: utf-8 -*-
# @Author  : ysl
# @File    : test.py
# @Time    : 2024/7/2 16:36
import requests


def get_data(cj, page=1):
    """Test cookie -> Check whether it can be used normally."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    }
    params = {
        '_': '1715759788665',
        'wemediaId': 'W4791101179257925736',
        'realUserId': 'dazhongrongmei@126.com',
    }
    data = {
        'pageNo': page,
        'size': '10',
        'contentType': '0',
        'contentState': '-1',
        'mergeUnPassed': 'false',
        'filterState': '0',
    }

    try:
        response = requests.post(
            'https://mp.163.com/wemedia/content/manage/list.do',
            params=params,
            cookies=cj,
            headers=headers,
            data=data,
        )
        response.raise_for_status()
        resp_json = response.json()
        data_list = resp_json.get('data', {}).get('list')
        if not data_list:
            print("No data returned.")
            return
        for con in data_list:
            title = con.get('title')
            print(f"Title: {title}")
    except requests.RequestException as e:
        print(f"Failed to get data: {e}")


def get_id(_id=0, ck=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    }
    url = "https://mp.yidianzixun.com/api/get-Article-id?id={}".format(_id)
    res = requests.get(url, headers=headers, cookies=ck)
    return res.json().get('result')


if __name__ == '__main__':
    import rookiepy

    cookies = rookiepy.chrome(["yidianzixun.com"])
    print(cookies)
    ck = dict()
    for cookie in cookies:
        dom = cookie['domain']
        ck[cookie['name']] = cookie['value']
    print(get_id(ck=ck))

