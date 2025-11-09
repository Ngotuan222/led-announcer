#!/usr/bin/env bash
# Script test LED với tự động chọn Python đúng

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_PYTHON="$PROJECT_ROOT/.venv/bin/python3"

cd "$PROJECT_ROOT"

# Kiểm tra venv python
if [ ! -f "$VENV_PYTHON" ]; then
    echo "✗ Virtual environment chưa được tạo"
    echo "   Chạy: ./scripts/install_dependencies.sh"
    exit 1
fi

# Kiểm tra xem có cần sudo không
NEED_SUDO=false
if ! groups | grep -q gpio; then
    NEED_SUDO=true
    echo "⚠️  User chưa trong group gpio, sẽ cần sudo"
fi

# Chạy test
if [ "$NEED_SUDO" = true ]; then
    echo "Đang chạy với sudo (sử dụng venv python)..."
    sudo "$VENV_PYTHON" scripts/test_led_simple.py
else
    echo "Đang chạy (không cần sudo)..."
    "$VENV_PYTHON" scripts/test_led_simple.py
fi

