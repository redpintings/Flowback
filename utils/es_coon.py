import sys
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from conf import Es
from loguru import logger
import threading

sys.path.append("/Users/ysl/dz_data_back")
sys.path.append("/opt/workstation/dz_data_back")


class EsConn:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
                    cls._instance._init_es()
        return cls._instance

    def _init_es(self):
        try:
            self.es = Elasticsearch(hosts=[f"http://{Es.username}:{Es.password}@{Es.host}:{Es.port}/"])
            logger.info("Elasticsearch client created successfully")
        except Exception as e:
            logger.error(f"Failed to create Elasticsearch client: {e}")
            raise

    def search_by_title(self, title):
        index_name = "news_info_v1"
        query = {
            "query": {
                "bool": {
                    "must": [
                        {"match": {"title": title}},
                        {"exists": {"field": "deliverTarget"}}
                    ]
                }
            }
        }

        try:
            result = self.es.search(index=index_name, body=query)
            news_ids = [hit["_source"]["newsId"] for hit in result["hits"]["hits"]]
            return news_ids
        except Exception as e:
            logger.error(f"Error searching by title: {e}")
            return []


if __name__ == '__main__':
    title_to_search = "“商”出为民情怀 “托”起未来希望"
    esc = EsConn()
    result_ids = esc.search_by_title(title_to_search)
    # Print the search results
    print(f"标题 '{title_to_search}' 对应的news_id: {result_ids}")
