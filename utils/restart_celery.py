#!/usr/bin/ python
# -*- coding: utf-8 -*-
# @Author  : ysl
# @File    : restart_celery.py

import time
from conf import celery_path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os


class ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print(f"{event.src_path} has been modified, restarting Celery...")
            os.system("sudo supervisorctl restart celery")


if __name__ == "__main__":
    path = celery_path
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
