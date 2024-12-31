#!/usr/bin/ python
# -*- coding: utf-8 -*-
# @Author  : ysl
# @File    : __init__.py

"""
Dify 项目研究
 gongzuoliu项目研究
 工作流 study
 索引 study
 医药 工作流文件索引

searxng 搜索引擎
searxng 结合dify项目，实现搜索引擎功能，包括：






智普longcite 项目
智普longcite 项目的主要功能是：
1. 128k上下文  引用
2. 总结性大模型


llamaindex RAG项目

llamaindex RAG项目的主要功能是：
1. 基于RAG的文本换向量 查询
已经跑完 domo：
demo 包含两部分，
（1）包含文本转向量  查询
（2）本地加载索引index -> 查询


RAg 智能体agent 学习研究


火山引擎创建智能体agent 研究
——————————————————————


ai 相关性研究文生图测试
生成短视频 测试效果不好， 目前国内没有很好的生成视频的软件都是图片合成的
图文融合模型测试调研

今天调研InstantX/InstantID生成图片, 单个gpu 在m10 单个8G上不能够运行 显存太小
尝试使用多gpu 运行失败， 再找其他办法了只能
催孙国磊对显卡进行检查 确认就是8g 的显存

4月20 - 5月初

目前在做新的数据回流的平台


#!/usr/bin/ python
# -*- coding: utf-8 -*-
# @Author  : ysl
# @File    : es_coon.py
import sys

sys.path.append("/Users/ysl/dz_data_back")
sys.path.append("/opt/workstation/dz_data_back")
# TODO
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
class Es:
    host = "192.168.0.195"
    port = 9200
    username = "admin"
    password = "Y9bkmC79f%232K"


# 创建Elasticsearch客户端

class EsConn:
    def __init__(self):
        self.es = Elasticsearch(hosts=[f"http://{Es.username}:{Es.password}@{Es.host}:{Es.port}/"])

    def search_by_title(self, title):
        # 在索引中进行匹配查询
        index_name = "news_info"  # Elasticsearch索引名称
        query = {
            "query": {
                "match": {
                    "title": title
                }
            }
        }
        # 执行查询
        result = self.es.search(index=index_name, body=query)
        news_ids = [hit["_source"]["newsId"] for hit in result["hits"]["hits"]]
        return news_ids


if __name__ == '__main__':
    # 例子：根据标题查询news_id
    title_to_search = "山东多地看房、买房的人都多了"
    esc = EsConn()
    result_ids = esc.search_by_title(title_to_search)

    # 输出查询结果
    print(f"标题 '{title_to_search}' 对应的news_id: {result_ids}")

"""