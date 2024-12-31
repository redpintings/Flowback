#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : ysl
# @File    : pipeline.py

import json
import pymongo
import asyncio
from tasks import Task
from settings import MONGO_URI, MONGO_DATABASE, DATA_FILE_PATH


class Pipeline:
    def __init__(self):
        # Initialize Task without creating Semaphore here
        self.task = Task()

    async def process_item(self, item):
        """
        Process the item by storing it in a file, MongoDB, and an API endpoint.
        """
        # Store item in file and MongoDB synchronously
        # self.store_in_file(item)
        # self.store_in_mongo(item)

        # Store item in API asynchronously
        await self.store_in_api(item)

    @staticmethod
    def store_in_file(item):
        """
        Store the item in a JSON file.
        """
        try:
            with open(DATA_FILE_PATH, 'a') as f:
                json.dump(item, f)
                f.write('\n')
        except Exception as e:
            print(f"Error storing item in file: {e}")

    @staticmethod
    def store_in_mongo(item):
        """
        Store the item in a MongoDB collection.
        """
        try:
            client = pymongo.MongoClient(MONGO_URI)
            db = client[MONGO_DATABASE]
            collection = db['items']
            collection.insert_one(item)
        except Exception as e:
            print(f"Error storing item in MongoDB: {e}")

    async def store_in_api(self, item):
        """
        Send the item to an API endpoint.
        """
        await self.task.send_msg(item)