#!/usr/bin/ python
# -*- coding: utf-8 -*-
# @Author  : ysl
# @File    : projectTree.py
import os


def print_python_files_tree(path, indent=0):
    """
    打印出给定路径下的.py文件和目录结构树，跳过venv目录。
    :param path: 要打印的目录路径。
    :param indent: 当前缩进级别。
    """
    if not os.path.isdir(path):
        print("错误：提供的路径不是目录")
        return

    for entry in os.listdir(path):
        entry_path = os.path.join(path, entry)
        if entry == 'venv' or entry.startswith('.') or entry.startswith('__'):
            # 跳过venv目录和隐藏文件/目录
            continue
        elif os.path.isfile(entry_path) and entry.endswith('.py'):
            print('  ' * indent + '|-- ' + entry)
        elif os.path.isdir(entry_path):
            print('  ' * indent + '|-- ' + entry)
            print_python_files_tree(entry_path, indent + 1)


if __name__ == '__main__':
    project_path = '/Users/ysl/Flowback'
    print_python_files_tree(project_path)
