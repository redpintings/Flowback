#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : ysl
# @File    : downloadMiddleware.py

import random
from loguru import logger
from . import settings
from Backflows.middleware import DownloadMiddleware


class UserAgentMiddleware(DownloadMiddleware):
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8',
        # Add more user agents
    ]

    async def process_request(self, request):
        user_agent = random.choice(self.USER_AGENTS)
        logger.warning(f'Using random user agent: {user_agent}')
        request.headers['User-Agent'] = user_agent
        return request


class RetryMiddleware(DownloadMiddleware):
    MAX_RETRIES = settings.MAX_RETRIES

    async def process_response(self, request, response):
        if response.status_code != 200 and request.meta.get('retry_times', 0) < self.MAX_RETRIES:
            retry_times = request.meta.get('retry_times', 0) + 1
            logger.warning(f"Retrying {request.url} (attempt {retry_times})")
            request.meta['retry_times'] = retry_times
            return await self.process_request(request)  # Retry the request
        return response


class ProxyMiddleware(DownloadMiddleware):
    PROXIES = [
        'http://proxy1.example.com:8000',
        'http://proxy2.example.com:8000',
        # Add more proxies
    ]

    async def process_request(self, request):
        proxy = random.choice(self.PROXIES)
        request.meta['proxy'] = proxy
        return request
