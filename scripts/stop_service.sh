#!/usr/bin/env bash
# Script dừng dịch vụ LED announcer

set -euo pipefail

PORT=${1:-8000}

echo "Đang tìm process đang chạy trên port $PORT..."

# Tìm PID của process đang dùng port
PID=$(lsof -ti :$PORT 2>/dev/null || echo "")

if [ -z "$PID" ]; then
    echo "Không có process nào đang chạy trên port $PORT"
    exit 0
fi

echo "Tìm thấy process PID: $PID"
ps -p $PID -o pid,user,cmd

read -p "Dừng process này? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    kill $PID
    sleep 1
    
    # Kiểm tra lại
    if lsof -ti :$PORT >/dev/null 2>&1; then
        echo "Process vẫn chạy, đang force kill..."
        kill -9 $PID
    fi
    
    echo "✓ Đã dừng process"
else
    echo "Hủy bỏ"
    exit 1
fi

