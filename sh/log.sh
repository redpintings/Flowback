#!/bin/bash

# 设置日志目录
LOG_DIR="/opt/workstation/dz_data_back/log"
# shellcheck disable=SC2164
cd $LOG_DIR

# 查找并压缩符合条件的日志文件
find . -type f -name 'celery_err.log.*' ! -name '*.gz' | while read -r file; do
    # 压缩文件
    gzip "$file"
    # 删除原文件
    if [ $? -eq 0 ]; then
        echo "Compressed and removed: $file"
    else
        echo "Failed to compress: $file"
    fi
done
