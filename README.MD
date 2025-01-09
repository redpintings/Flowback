<div align="center">
    <h1>Backflow</h1>
</div>

<div align="center">
    <a href="https://github.com/redpintings/Flowback">
        <img alt="GitHub Actions Workflow Status" src="https://image.dzplus.dzng.com/2025/01/09/17364137282465.jpg" />
    </a>
</div>

<div align="center">
    <a href="https://pypi.org/project/backflow/">
        <img alt="PyPI Version" src="https://image.dzplus.dzng.com/2024/06/06/17176696807966.jpg" />
    </a>
    <a href="https://github.com/redpintings/Flowback/issues">
        <img alt="GitHub Issues" src="https://image.dzplus.dzng.com/2024/06/06/17176697207099.jpg" />
    </a>
    <a href="https://github.com/redpintings/Flowback">
        <img alt="GitHub Repository" src="https://image.dzplus.dzng.com/2024/06/06/17176697507539.jpg" />
    </a>
</div>

Backflow 是一个简洁且灵活的爬虫框架，支持使用 Celery 实现分布式爬取。你可以根据自己的需求编写爬虫代码，并且框架提供了丰富的配置选项和扩展能力。

## 目录

- [🎯 功能](#功能)
- [💻 运行平台](#运行平台)
- [🔧 运行环境](#运行环境)
- [🏃‍ Quick Start](#quick-start)
    - [安装依赖](#安装依赖)
    - [修改配置文件](#修改配置文件)
    - [运行程序](#运行程序)
    - [分布式运行](#分布式运行)
    - [添加新爬虫](#添加新爬虫)
- [💼 服务器配置](#服务器配置)
- [🕷️ 爬虫代码模板](#爬虫代码模板)
- [👨 框架运行步骤](#框架运行步骤)
- [❓ 注意事项](#注意事项)

## 功能

- 支持单机多线程爬取
- 支持分布式爬取（基于 Celery）
- 灵活的配置选项
- 易于扩展的爬虫模板

## 运行平台

- [x] Linux
- [x] macOS
- [x] Windows

## 运行环境

- Python 3.9+
- Linux / Windows

## Quick Start

### 安装依赖

```bash
pip install backflow
```

#### 修改配置文件conf And settings

```yaml
celery:
  host: 127.0.0.1
  port: 27017
  xxxx: xxxx

es:
  host: 127.0.0.1
  port: 9200
...

```

#### 运行程序

```bash
# 查看命令帮助
backflow --help
# 查看目前所有的回流平台的爬虫列表
backflow list
# 运行单个爬虫
backflow crawl baijiahao  # Single run
backflow crawl jinritoutiao  # Single run

# Single run  The default is 20 pages. If you want to set page numbers, use the --page parameter
# For detailed parameters, please refer to the default parameter START_PAGE END_PAGE PAGE_STEP in settings.py
backflow crawl baijiahao --page 4  
# 运行所有爬虫 多线程单机运行
# main_back.py  # Can run all crawlers

```

#### 分布式运行 Execute Cellery Distributed

```bash
 # 启动celery worker
celery -A tasks worker --loglevel=info 

# run distributed command / 分布式运行
backflow crawl baijiahao --distributed

# if you need to specify the number of pages for a distributed crawler, 100 pages, and a step size of 10
backflow crawl baijiahao --distributed --page 100 --step 10

```

#### 添加新爬虫 新增名为newspider的爬虫

```bash
# add new spider
backflow addspider newspider

```


### 模版爬虫代码

  > 当你使用命令`backflow addspider newspider`创建好一个新的spider模版后，请确保你的爬虫代码请求 可以正确采集到数据

```python
from loguru import logger
from utils.tools import Tools
from Backflows.base import BackFlow
from Backflows.middleware import Request
import traceback


class {spider_name.capitalize()}(BackFlow):
    name = '{spider_name}'

    def __init__(self):
        super().__init__()
        self.ck = None
        self.headers = {{
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like "
                          "Gecko) Chrome/108.0.0.0 Safari/537.36"
        }}

    async def get_page_request(self, page):
        url = 'http://example.com/api/data?page={{}}'.format(page)
        return Request('GET', url=url, headers=self.headers, cookies=self.ck, meta={{'page': page}})

    async def parse(self, response):

        resp = response.json()
        datas = resp.get('data', {{}})
        if not datas:
            print(f'{spider_name} cookie might be expired or no data returned.')
            return
        for con in datas:
            news = {{
                'url': con.get('item_id', ''),
            }}
            yield news

```

### 正式服务器配置

```yaml
server:
  120.xx.xx.249

demo server:
  host: 120.xx.xx.249
  path: /opt/workstation/xx/

定时任务:
  crontab/supervisor

```
### 框架运行步骤


1. **启动程序**：
   在命令行中运行`runner.py`，并传入相应的参数，例如爬虫的名称、是否以分布式模式运行、停止页码和步长。

2. **命令行解析**：
   `argparse`库解析命令行参数，并根据参数确定运行模式。

3. **查找爬虫**：
   `SpiderRunner`类的`find_spiders`方法搜索所有已定义的爬虫模块（如`spiders`），并导入这些模块。它查找所有继承自`BackFlow`类的爬虫，并将它们存储在一个字典中，键为爬虫的名称。

4. **加载中间件&&Settings**：
   `load_middlewares`方法根据`settings.MIDDLEWARES`配置加载中间件。中间件包括用户代理、重试和代理中间件，它们用于修改请求和处理响应。

5. **运行爬虫**：
   如果选择了分布式模式，`run`方法会为每个页面生成一个`run_spider`任务，并使用Celery将其添加到任务队列中。否则，它会为每个页面创建一个异步任务，并使用`asyncio.gather`等待所有任务完成。

6. **执行任务**：
   在分布式模式下，Celery worker会从任务队列中获取任务并执行。每个任务都会调用`async_run_spider`异步函数。

7. **获取页面请求**：
   `async_run_spider`函数会创建一个`Page`对象，并调用爬虫的`get_page_request`方法来获取该页面的请求对象。

8. **处理请求**：
   `process_request`方法使用中间件处理请求，例如添加用户代理、设置代理等。

9. **抓取页面**：
   `fetch_page`方法使用`httpx.AsyncClient`发送请求并获取响应。它使用信号量来限制并发请求数量。

10. **处理响应**：
    `process_response`方法使用中间件处理响应，例如检查响应状态码。

11. **解析页面**：
    爬虫的`parse`方法解析响应内容，提取数据项。对于每个提取的数据项，它会调用管道的`process_item`方法进行处理。

12. **管道处理数据项**：
    Pipeline的`process_item`方法将数据项存储到MongoDB或文件中。

13. **统计信息**：
    爬虫会更新已抓取页面数和已发送请求数。在所有页面抓取完成后，`print_stats`方法会打印这些统计信息。

14. **错误处理**：
    如果任何步骤出现错误，异常会被捕获，错误信息会被记录，并通过钉钉发送通知。


### 注意事项

- 本项目仅供学习交流使用，未经本地测试 请不要在生产环境使用。
- 分布式运行需要启动celery worker。
- restart_celery.py 脚本用于监控并重启celery worker。需要在supervisor中配置或者 直接运行
- 爬虫代码需要在backflow/spiders目录下。
- 爬虫配置文件需要在backflow/conf目录 和 backflow/settings.py中配置。