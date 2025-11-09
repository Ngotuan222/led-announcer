#!/usr/bin/env bash
# Script khởi động dịch vụ LED announcer

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PORT=${1:-8000}

cd "$PROJECT_ROOT"

# Kiểm tra port có đang được sử dụng không
if lsof -ti :$PORT >/dev/null 2>&1; then
    echo "⚠️  Port $PORT đang được sử dụng"
    echo "   Đang dừng process cũ..."
    ./scripts/stop_service.sh $PORT
    sleep 1
fi

# Kiểm tra virtual environment
if [ ! -f ".venv/bin/activate" ]; then
    echo "✗ Virtual environment chưa được tạo"
    echo "   Chạy: ./scripts/install_dependencies.sh"
    exit 1
fi

# Kích hoạt virtual environment
source .venv/bin/activate

# Kiểm tra thư viện rgbmatrix (cảnh báo nhưng không dừng)
if ! python3 -c "from rgbmatrix import RGBMatrix" 2>/dev/null; then
    echo "⚠️  Cảnh báo: Thư viện rgbmatrix chưa được cài đặt"
    echo "   LED sẽ không hoạt động, chỉ có audio"
    echo "   Cài đặt: ./scripts/install_rgb_matrix.sh"
    echo ""
fi

echo "Đang khởi động dịch vụ trên port $PORT..."
echo "Nhấn Ctrl+C để dừng"
echo ""

uvicorn src.main:app --host 0.0.0.0 --port $PORT

