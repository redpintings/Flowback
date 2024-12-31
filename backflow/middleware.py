#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : ysl
# @File    : middleware.py

class DownloadMiddleware:
    async def process_request(self, request):
        return request

    async def process_response(self, request, response):
        return response


class MiddlewareManager:
    def __init__(self, middlewares):
        self.middlewares = middlewares

    async def process_request(self, request):
        for middleware in self.middlewares:
            request = await middleware.process_request(request)
        return request

    async def process_response(self, request, response):
        for middleware in self.middlewares:
            response = await middleware.process_response(request, response)
        return response


class Request:
    def __init__(self, method, url, headers=None, data=None, proxies=None, params=None, meta=None, cookies=None):
        self.method = method
        self.url = url
        self.headers = headers or {}
        self.data = data
        self.proxies = proxies
        self.meta = meta or {}
        self.params = params or {}
        self.cookies = cookies or {}