#!/bin/bash

# 检查Python解释器路径
if [ -x "/Users/ysl/dz_data_back/venv/bin/python" ]; then
    PYTHON_PATH="/Users/ysl/dz_data_back/venv/bin/python"
    CHECK_PY_PATH="/Users/ysl/dz_data_back/sh/check.py"
elif [ -x "/root/anaconda3/bin/python" ]; then
    PYTHON_PATH="/root/anaconda3/bin/python"
    CHECK_PY_PATH="/opt/workstation/dz_data_back/sh/check.py"
else
    echo "No valid Python interpreter or check.py found."
    exit 1
fi

# shellcheck disable=SC2164
cd /opt/workstation/dz_data_back

# 定义一个函数来处理命令执行和错误处理
run_command() {
    local command="$1"
    # 执行命令并捕获输出
    output=$(eval "$command" 2>&1)
    # shellcheck disable=SC2034
    local status=$?
    echo "$output"

    # 检查输出中是否包含错误字符串
    if [[ $output == *"cookie might be expired"* ]] || [[ $output == *"An error occurred while parsing"* ]]; then
        echo "Command failed: $command"
        $PYTHON_PATH $CHECK_PY_PATH send_dingding_alert "$command"
    fi
}

# 执行命令并处理错误
run_command "/root/anaconda3/bin/backflow crawl xinlangkandian --page 2"
run_command "/root/anaconda3/bin/backflow crawl baijiahao --page 2"
run_command "/root/anaconda3/bin/backflow crawl jinritoutiao --page 11 --step 10"
run_command "/root/anaconda3/bin/backflow crawl wangyi --page 2"
run_command "/root/anaconda3/bin/backflow crawl yidianzixun --page 2"
