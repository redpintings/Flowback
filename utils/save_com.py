#!/usr/bin/ python
# -*- coding: utf-8 -*-
# @Time    : 2024/02/01 16:00:00
# @Author  : ysl
# @File    : save_com.py
import sys

sys.path.append("/Users/ysl/dz_data_back")
sys.path.append("/opt/workstation/dz_data_back")
import asyncio
import aiohttp
from conf import save_com
from typing import List
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential


class Com:
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def com(self, parameter, item_id):
        data = {
            "topicTypeEnum": "NEWS",
            "topicId": item_id, # 新闻id
            "content": parameter.get("content"),  # 这是评论内容
            "bigDataHeadImage": parameter.get("user_avatar"),  # 头像地址
            "bigDataNickName": parameter.get("user_name"),  # 评论的昵称
            "bigDataPlatName": parameter.get("source"),  # 评论的平台名称
            "createTime": parameter.get("comment_time"),  # 评论时间
        }
        logger.info(f'Save Comments FormData:{data} *org*:{parameter}')
        async with aiohttp.ClientSession() as session:
            async with session.post(save_com, json=data, timeout=30) as response:
                resp = await response.json()
                print(resp)
                return resp

    async def save_com(self, comments: List, item_id: str):
        tasks = [self.com(comment, item_id) for comment in comments]
        return await asyncio.gather(*tasks)


if __name__ == '__main__':
    cc = {'pv': 58968, 'comments': [{'content': '转发了',
                                     'user_avatar': 'https://sf1-cdn-tos.toutiaostatic.com/img/user-avatar/47d09642545413079f101c67d6765002~300x300.image',
                                     'source': '头条', 'user_name': '牧羊人的心仰sjx',
                                     'source_news_id': '7328268615734985225'}, {'content': '转发了',
                                                                                'user_avatar': 'https://sf3-cdn-tos.toutiaostatic.com/img/user-avatar/1473a6f26bf602b797b7e4180f397c76~300x300.image',
                                                                                'source': '头条',
                                                                                'user_name': '想蹦就跳',
                                                                                'source_news_id': '7328268615734985225'},
                                    {'content': '转发了',
                                     'user_avatar': 'https://sf1-cdn-tos.toutiaostatic.com/img/mosaic-legacy/3795/3047680722~300x300.image',
                                     'source': '头条', 'user_name': '用户1886283630958',
                                     'source_news_id': '7328268615734985225'}, {'content': '转发了',
                                                                                'user_avatar': 'https://sf6-cdn-tos.toutiaostatic.com/img/user-avatar/172bda9787251e7d3745ec33451836f0~300x300.image',
                                                                                'source': '头条',
                                                                                'user_name': '正能量苹果来自胶州',
                                                                                'source_news_id': '7328268615734985225'},
                                    {'content': '他爹还有37亿么😵',
                                     'user_avatar': 'https://sf1-cdn-tos.toutiaostatic.com/img/user-avatar/ed9cd1d217486b8dcb0b3603e2b57d65~300x300.image',
                                     'source': '头条', 'user_name': '甘露渴时一滴如甘露',
                                     'source_news_id': '7328268615734985225'}, {'content': '转发了',
                                                                                'user_avatar': 'https://sf3-cdn-tos.toutiaostatic.com/img/user-avatar/b07a8b89fb9e957fc00b02930af5798e~300x300.image',
                                                                                'source': '头条',
                                                                                'user_name': '跨界协汇在中国',
                                                                                'source_news_id': '7328268615734985225'},
                                    {'content': '转发了',
                                     'user_avatar': 'https://sf6-cdn-tos.toutiaostatic.com/img/user-avatar/7e70d40d7aff021493ca07abfb9325d7~300x300.image',
                                     'source': '头条', 'user_name': '德才兼备海洋舅舅',
                                     'source_news_id': '7328268615734985225'}]}
    bjh = {'pv': 155, 'comments': [{'content': '感谢比亚迪@@@@@，没有国产车，他们会卖50万',
                                    'user_avatar': 'https://himg.bdimg.com/sys/portrait/item/wise.1.db228224.d-hkSy20I4CQ9sj0Zk8c2g.jpg?time=3921&tieba_portrait_time=3921',
                                    'user_name': '百度网友7b3c801', 'comment_time': '1672991513', 'source': '百家号',
                                    'source_news_id': '1754258024237278742',
                                    'news_hash_id': 'ccf0ef3f062caad2c3710019961f7da6',
                                    'source_comment_id': '1121620250144030806'}, {'content': '国产车没压力，涨价就行了',
                                                                                  'user_avatar': 'https://himg.bdimg.com/sys/portrait/item/wise.1.eb0fcc5b.aQw7WTdTE0Nkp5r3_0d-HA.jpg?time=7728&tieba_portrait_time=7728',
                                                                                  'user_name': '小驴大嘴',
                                                                                  'comment_time': '1672992479',
                                                                                  'source': '百家号',
                                                                                  'source_news_id': '1754258024237278742',
                                                                                  'news_hash_id': 'ccf0ef3f062caad2c3710019961f7da6',
                                                                                  'source_comment_id': '1121620346667971904'},
                                   {'content': '试图拿价格对冲安全隐患',
                                    'user_avatar': 'https://himg.bdimg.com/sys/portrait/item/wise.1.12109c7a.lwNa1x_9pfTMECjrmftI1Q.jpg?time=10414&tieba_portrait_time=10414',
                                    'user_name': '兆云韶CC', 'comment_time': '1672991373', 'source': '百家号',
                                    'source_news_id': '1754258024237278742',
                                    'news_hash_id': 'ccf0ef3f062caad2c3710019961f7da6',
                                    'source_comment_id': '1121620236077081304'},
                                   {'content': '没有特斯@@@@@拉，比亚迪也有可能会卖50万[抠鼻]',
                                    'user_avatar': 'https://himg.bdimg.com/sys/portrait/item/wise.1.e04eddc.Cu_TJUsP9-U02SNRvApMcA.jpg?time=6121&tieba_portrait_time=6121',
                                    'user_name': '百度网友f461e93e7', 'comment_time': '1672992365', 'source': '百家号',
                                    'source_news_id': '1754258024237278742',
                                    'news_hash_id': 'ccf0ef3f062caad2c3710019961f7da6',
                                    'source_comment_id': '1121620335297354705'}, {'content': '比亚迪啥时候降价呀',
                                                                                  'user_avatar': 'https://himg.bdimg.com/sys/portrait/item/wise.1.f7b1fde8.K-wPBfnK9N0IO4Zx55u5Bw.jpg?time=3940&tieba_portrait_time=3940',
                                                                                  'user_name': '有一个大侠',
                                                                                  'comment_time': '1673070997',
                                                                                  'source': '百家号',
                                                                                  'source_news_id': '1754258024237278742',
                                                                                  'news_hash_id': 'ccf0ef3f062caad2c3710019961f7da6',
                                                                                  'source_comment_id': '1121628198507924708'},
                                   {'content': '就这？这还没到头呢，20多万为啥不买汉呢',
                                    'user_avatar': 'https://himg.bdimg.com/sys/portrait/item/wise.1.4235dfd2.cgJeyiPlKY6IBnIkmPQGcg.jpg?time=4878&tieba_portrait_time=4878',
                                    'user_name': '城市小光', 'comment_time': '1672991536', 'source': '百家号',
                                    'source_news_id': '1754258024237278742',
                                    'news_hash_id': 'ccf0ef3f062caad2c3710019961f7da6',
                                    'source_comment_id': '1121620252463400201'},
                                   {'content': '让车全面降价在@@@@@@@1全世界才有竟争力。',
                                    'user_avatar': 'https://himg.bdimg.com/sys/portrait/item/wise.1.9198812d.tGaMHXCrNgXFdeH745dREg.jpg?time=12832&tieba_portrait_time=12832',
                                    'user_name': '黎明euL', 'comment_time': '1673072537', 'source': '百家号',
                                    'source_news_id': '1754258024237278742',
                                    'news_hash_id': 'ccf0ef3f062caad2c3710019961f7da6',
                                    'source_comment_id': '1121628352540777507'}, {'content': '买涨不买跌[汗]',
                                                                                  'user_avatar': 'https://himg.bdimg.com/sys/portrait/item/wise.1.ea19030b.E88Xo8YcadTXDgiPKVRxlQ.jpg?time=3229&tieba_portrait_time=3229',
                                                                                  'user_name': 'ks55259980',
                                                                                  'comment_time': '1672991302',
                                                                                  'source': '百家号',
                                                                                  'source_news_id': '1754258024237278742',
                                                                                  'news_hash_id': 'ccf0ef3f062caad2c3710019961f7da6',
                                                                                  'source_comment_id': '1121620229031010802'},
                                   {'content': '棺材车，坚决抵制，滚出中国。',
                                    'user_avatar': 'https://himg.bdimg.com/sys/portrait/item/wise.1.f8261467.vAjE2pnNfGClK55yt_wOEA.jpg?time=4918&tieba_portrait_time=4918',
                                    'user_name': '祝愿大众破产', 'comment_time': '1673071429', 'source': '百家号',
                                    'source_news_id': '1754258024237278742',
                                    'news_hash_id': 'ccf0ef3f062caad2c3710019961f7da6',
                                    'source_comment_id': '1121628241723565004'}, {'content': '性价比不高',
                                                                                  'user_avatar': 'https://himg.bdimg.com/sys/portrait/item/wise.1.2b2169ea.2k3bmFXHz-UzFs6LnX95LA.jpg?time=4271&tieba_portrait_time=4271',
                                                                                  'user_name': '接念云U2',
                                                                                  'comment_time': '1673071414',
                                                                                  'source': '百家号',
                                                                                  'source_news_id': '1754258024237278742',
                                                                                  'news_hash_id': 'ccf0ef3f062caad2c3710019961f7da6',
                                                                                  'source_comment_id': '1121628240258204109'},
                                   {'content': '特斯拉干得漂亮，app造车的蔚来理想小鹏都快活不下去了',
                                    'user_avatar': 'https://himg.bdimg.com/sys/portrait/item/wise.1.933b4aa5.AUFaLVGyUP_nk7hsrnHAEg.jpg?time=6223&tieba_portrait_time=6223',
                                    'user_name': '徐朱墨', 'comment_time': '1673140222', 'source': '百家号',
                                    'source_news_id': '1754258024237278742',
                                    'news_hash_id': 'ccf0ef3f062caad2c3710019961f7da6',
                                    'source_comment_id': '1121635121051611603'},
                                   {'content': '华为和苹果一个价格，恐怕卖不出几部。',
                                    'user_avatar': 'https://gips0.baidu.com/it/u=655990077,265805602&fm=3012&app=3012&autime=1688006895&size=b200,200',
                                    'user_name': '草莓物理植保', 'comment_time': '1673071812', 'source': '百家号',
                                    'source_news_id': '1754258024237278742',
                                    'news_hash_id': 'ccf0ef3f062caad2c3710019961f7da6',
                                    'source_comment_id': '1121628280014230202'},
                                   {'content': '没有补贴了，国产电动车性价比能行吗？',
                                    'user_avatar': 'https://himg.bdimg.com/sys/portrait/item/wise.1.6bea4fe9.lD_wan5o13mMqDLNs24zKQ.jpg?time=4947&tieba_portrait_time=4947',
                                    'user_name': '青岛海螺号', 'comment_time': '1673071792', 'source': '百家号',
                                    'source_news_id': '1754258024237278742',
                                    'news_hash_id': 'ccf0ef3f062caad2c3710019961f7da6',
                                    'source_comment_id': '1121628278025421804'},
                                   {'content': '切实，现在电动汽车价格是越来越高[左捂脸]',
                                    'user_avatar': 'https://gips0.baidu.com/it/u=2420953407,791959124&fm=3012&app=3012&autime=1693365062&size=b200,200',
                                    'user_name': '金门高粱酒旅游人', 'comment_time': '1673063596', 'source': '百家号',
                                    'source_news_id': '1754258024237278742',
                                    'news_hash_id': 'ccf0ef3f062caad2c3710019961f7da6',
                                    'source_comment_id': '1121627458444463108'}, {'content': '和苹果手机一个套路',
                                                                                  'user_avatar': 'https://himg.bdimg.com/sys/portrait/item/wise.1.2791c06b.ArKHWPG1gSl2MXBUhXmB7w.jpg?time=1829&tieba_portrait_time=1829',
                                                                                  'user_name': '午马未羊Di',
                                                                                  'comment_time': '1673019020',
                                                                                  'source': '百家号',
                                                                                  'source_news_id': '1754258024237278742',
                                                                                  'news_hash_id': 'ccf0ef3f062caad2c3710019961f7da6',
                                                                                  'source_comment_id': '1121623000803493301'}],
           'news_hash_id': 'ccf0ef3f062caad2c3710019961f7da6'}
    com = Com()

    # asyncio.run(com.save_com(cc['comments']))

    # For Python 3.6 and below
    loop = asyncio.get_event_loop()
    loop.run_until_complete(com.save_com(bjh['comments'], '1324567890'))
    loop.close()
