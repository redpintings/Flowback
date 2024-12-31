#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : ysl
# @File    : link.py
import logging
import os
import signal
import sys
import re
import chardet
import urllib3
import requests
import tldextract
from loguru import logger
from bs4 import BeautifulSoup
from lxml import html
from urllib.parse import urlparse, urljoin
from logging.handlers import RotatingFileHandler
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from concurrent.futures import ThreadPoolExecutor

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class LinkSpider:
    def __init__(self, allow_domains=None, deny_domains=None, depth=1, method='bs4', pattern=None, current_depth=1,
                 headers=None, cookies=None, max_workers=10):
        """
        Initialize the LinkSpider with optional domain filters and depth.
        """
        self.allow_domains = allow_domains or []
        self.deny_domains = deny_domains or []
        self.depth = depth
        self.method = method
        self.pattern = pattern
        self.current_depth = current_depth
        self.headers = headers
        self.cookies = cookies
        self.visited_links = set()
        self.max_workers = max_workers
        self.charset = 'utf-8'
        self.session = self._setup_session()

    def _setup_session(self):
        session = requests.Session()
        retries = Retry(total=4, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
        session.mount('http://', HTTPAdapter(max_retries=retries))
        session.mount('https://', HTTPAdapter(max_retries=retries))
        return session

    def extract_links(self, html_content, base_url, method='bs4', pattern=None):
        """
        Extract links from the given HTML content using the specified method.
        """
        if method == 'bs4':
            return self._extract_links_bs4(html_content, base_url)
        elif method == 'xpath':
            return self._extract_links_xpath(html_content, base_url, pattern)
        elif method == 're':
            return self._extract_links_regex(html_content, base_url, pattern)
        else:
            raise ValueError("Unsupported method. Use 'bs4', 'xpath', or 'regex'.")

    def _extract_links_bs4(self, html_content, base_url):
        """
        Extract links using BeautifulSoup.
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        links = [urljoin(base_url, a['href']) for a in soup.find_all('a', href=True)]
        return self._filter_links(links)

    def _extract_links_xpath(self, html_content, base_url, xpath_expr):
        """
        Extract links using XPath.
        """
        tree = html.fromstring(html_content)
        links = [urljoin(base_url, link) for link in tree.xpath(xpath_expr)]
        return self._filter_links(links)

    def _extract_links_regex(self, html_content, base_url, regex_pattern):
        """
        Extract links using regular expressions.
        """
        links = [urljoin(base_url, link) for link in re.findall(regex_pattern, html_content)]
        return self._filter_links(links)

    def _filter_links(self, links):
        """
        Filter links based on allow_domains and deny_domains.
        """
        filtered_links = []
        for link in links:
            if not link.startswith(('http://', 'https://')):
                continue
            domain = tldextract.extract(link).registered_domain
            if self.allow_domains and domain not in self.allow_domains:
                continue
            if self.deny_domains and domain in self.deny_domains:
                continue
            if link in self.visited_links:
                continue
            self.visited_links.add(link)
            filtered_links.append(link)
        return filtered_links

    def parse(self, response, current_depth=None):
        """
        Parse the response object and extract links using the specified method.
        """
        if current_depth is None:
            current_depth = self.current_depth

        encoding = chardet.detect(response.content).get('encoding')
        response.encoding = encoding if encoding else self.charset
        html_content = response.text
        base_url = response.url
        links = self.extract_links(html_content, base_url, self.method, self.pattern)

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = []
            for link in links:
                yield link
                if current_depth < self.depth:
                    futures.append(executor.submit(self.fetch_and_parse, link, current_depth + 1))
            for future in futures:
                try:
                    yield from future.result()
                except Exception as e:
                    logger.error(f"Error processing future: {e}")

    def fetch_and_parse(self, url, current_depth):
        """
        Fetch the URL and parse the response.
        """
        try:
            new_response = self.session.get(url, headers=self.headers, verify=False, cookies=self.cookies)
            if new_response.status_code == 200:
                return list(self.parse(new_response, current_depth))
            else:
                logger.error(f"Failed to fetch {url}: {new_response.status_code}")
        except requests.RequestException as e:
            logger.error(f"Failed to fetch {url}: {e}")
        return []


# Example usage:
if __name__ == "__main__":
    start_url = 'https://www.toutiao.com/'
    spider = LinkSpider(allow_domains=['toutiao'], depth=2)
    try:
        response = requests.get(start_url, verify=False)
        for link in spider.parse(response):
            if link.endswith('html'):
                print(link)
    except requests.RequestException as e:
        logger.error(f"Failed to start crawling: {e}")