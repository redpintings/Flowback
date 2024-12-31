#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : ysl
# @File    : check.py

import argparse
import asyncio
import requests
from utils.monitor import SendMsg
from utils.ding import send_dingding
from loguru import logger


def send_sms_alert(source_name):
    logger.error(f"Send mobile msg: {source_name} did not return any data.")
    SendMsg().send_message(source_name)


async def send_dingding_alert(source_name):
    logger.error(f"Send dingding msg: {source_name} did not return any data. cookie 失效")
    await send_dingding(f"@杨士龙 {source_name} did not return any data. 可能 cookie 失效.")


async def main():
    parser = argparse.ArgumentParser(description="Check and alert script.")
    parser.add_argument('function', type=str, help="Function to call")
    parser.add_argument('source_name', default='123', type=str, help="Source name to pass to the function")

    args = parser.parse_args()

    if args.function == "send_sms_alert":
        send_sms_alert(args.source_name)
    elif args.function == "send_dingding_alert":
        await send_dingding_alert(args.source_name)
    else:
        logger.error(f"Unknown function: {args.function}")


if __name__ == "__main__":
    asyncio.run(main())
