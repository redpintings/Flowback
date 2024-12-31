#!/usr/bin/ python
# -*- coding: utf-8 -*-
# @Time    : 2020-09-01 14:16
# @Author  : ysl
# @Site    : 
# @File    : emoji.py
# @Software: PyCharm
from .static import *
import json
import re
import os


class Emoji(object):

    def __init__(self):
        self.dict_obj = self.dict_to_obj()

    class Dict(dict):
        __setattr__ = dict.__setitem__
        __getattr__ = dict.__getitem__

    def dict_to_object(self, dict_obj):
        if not isinstance(dict_obj, dict):
            return dict_obj
        inst = self.Dict()
        for k, v in dict_obj.items():
            inst[k] = self.dict_to_object(v)
        return inst

    def dict_to_obj(self, fn='/opt/workspace/spider_update/spider_update/emojis/emoji.json'):
        is_exists = os.path.exists(fn)
        em_obj_list = []
        if is_exists:
            json_data = json.load(open(fn, encoding='utf-8'))
            for i in range(len(json_data)):
                em_obj = self.dict_to_object(json_data[i])
                em_obj_list.append(em_obj)
        return em_obj_list

    @staticmethod
    def find_emoji(emoji, dict_to_obj):
        em_obj_list = dict_to_obj
        for i in em_obj_list:
            if emoji == i.codes:
                return i
        # 返回一个带有默认值的对象
        default_obj = Emoji.Dict()
        default_obj.char = ''
        return default_obj

    def parse_emoji(self, data):
        msg = re.findall(r'(\[.*?\])', data)
        for ms in msg:
            if len(ms) > 6:
                continue
            _em = EMOJI.get(ms, '1F604')
            _em = self.find_emoji(_em, self.dict_obj)
            data = data.replace(ms, _em.char)
        return data
