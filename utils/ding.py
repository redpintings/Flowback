# -*- coding: utf-8 -*-
# @Author  : ysl
# @File    : ding.py

import traceback
import asyncio
import httpx
from tenacity import retry, stop_after_attempt, wait_fixed, before_log, after_log


# Send DingDing message
@retry(stop=stop_after_attempt(2), wait=wait_fixed(10))
async def send_dingding(msg):
    url = "xx"
    headers = {'x-token': "xx"}
    data = {
        "content": msg
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=data)
            response.raise_for_status()  # Raise an exception for HTTP errors
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            raise  # Re-raise the exception to trigger a retry
        except Exception as e:
            print(f"An error occurred: {e}")
            raise  # Re-raise the exception to trigger a retry


if __name__ == '__main__':
    asyncio.run(send_dingding("test 12111"))
