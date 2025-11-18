#!/bin/bash

# Script cài đặt tự động LED Announcer từ GitHub
# Dành cho Raspberry Pi OS

set -e  # Dừng script nếu có lỗi

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MODE="${1:---auto}"

show_usage() {
    cat <<'EOF'
Usage: ./scripts/setup_from_git.sh [--auto|--manual|--help]

Options:
  --auto    (mặc định) chạy toàn bộ quá trình cài đặt tự động
  --manual  chỉ in ra hướng dẫn cài đặt thủ công để bạn chủ động thực hiện
  --help    hiển thị trợ giúp
EOF
}

show_manual_steps() {
    cat <<'EOF'
📋 Các bước cài đặt thủ công:
1. sudo apt update && sudo apt upgrade -y
2. sudo apt install -y python3-pip python3-venv build-essential python3-dev git mpg123 curl cython3
3. cd ~ && git clone https://github.com/hzeller/rpi-rgb-led-matrix.git
4. cd ~/rpi-rgb-led-matrix && make build-python && sudo make install-python
5. cd ~/led-announcer && python3 -m venv .venv && source .venv/bin/activate
6. pip install --upgrade pip && pip install -r requirements.txt
7. chmod +x scripts/*.sh scripts/*.py
8. python3 scripts/test_led_simple.py (kiểm tra LED) / ./scripts/start_service.sh (chạy dịch vụ)

Bạn có thể thực hiện từng bước để tùy chỉnh linh hoạt (ví dụ đổi thư mục, tùy chỉnh package).
EOF
}

require_non_root() {
    if [[ $EUID -eq 0 ]]; then
        echo "❌ Đừng chạy script này với quyền root (sudo)"
        echo "👉 Chạy với user thường: ./scripts/setup_from_git.sh"
        exit 1
    fi
}

check_internet() {
    echo "🌐 Kiểm tra kết nối internet..."
    if ! ping -c 1 google.com &> /dev/null; then
        echo "❌ Không có kết nối internet. Vui lòng kiểm tra lại."
        exit 1
    fi
}

setup_system_packages() {
    echo "📦 Updating system packages..."
    sudo apt update
    sudo apt upgrade -y

    echo "🔧 Installing required packages..."
    sudo apt install -y python3-pip python3-venv build-essential python3-dev git mpg123 curl cython3
}

install_rgb_led_matrix() {
    echo "🔌 Installing rpi-rgb-led-matrix library..."
    if [ ! -d "$HOME/rpi-rgb-led-matrix" ]; then
        echo "Cloning rpi-rgb-led-matrix..."
        git clone https://github.com/hzeller/rpi-rgb-led-matrix.git "$HOME/rpi-rgb-led-matrix"
    else
        echo "rpi-rgb-led-matrix already exists, updating..."
        (cd "$HOME/rpi-rgb-led-matrix" && git pull)
    fi

    echo "Building and installing rpi-rgb-led-matrix..."
    (cd "$HOME/rpi-rgb-led-matrix" && make build-python && sudo make install-python)
}

setup_python_env() {
    cd "$PROJECT_ROOT"
    echo "🐍 Creating Python virtual environment..."
    if [ ! -d ".venv" ]; then
        python3 -m venv .venv
    fi

    echo "📚 Installing Python dependencies..."
    source .venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
}

check_font() {
    echo "🔤 Checking font availability..."
    FONT_PATH="$HOME/rpi-rgb-led-matrix/fonts/10x20.bdf"
    if [ ! -f "$FONT_PATH" ]; then
        echo "⚠️  Font not found at $FONT_PATH"
        echo "🔍 Creating fonts directory"
        sudo mkdir -p "$HOME/rpi-rgb-led-matrix/fonts/"
        echo "Font sẽ được tạo tự động khi chạy test lần đầu"
    fi
}

run_tests() {
    cd "$PROJECT_ROOT"
    echo "🔐 Setting up permissions..."
    chmod +x scripts/*.sh
    chmod +x scripts/*.py

    echo "🧪 Testing installation..."
    source .venv/bin/activate

    python3 -c "
import sys
try:
    import fastapi
    import uvicorn
    import gtts
    import yaml
    print('✅ Python dependencies OK')
except ImportError as e:
    print(f'❌ Python dependency error: {e}')
    sys.exit(1)
"

    python3 -c "
import sys
try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions
    print('✅ rpi-rgb-led-matrix OK')
except ImportError as e:
    print(f'❌ rpi-rgb-led-matrix error: {e}')
    print('🔧 You may need to run with sudo for LED access')
    sys.exit(1)
"
}

print_next_steps() {
    echo ""
    echo "🎉 Cài đặt hoàn tất!"
    echo ""
    echo "📋 Các bước tiếp theo:"
    echo "1. Kiểm tra phần cứng:"
    echo "   python3 scripts/test_led_simple.py"
    echo ""
    echo "2. Test hiển thị text:"
    echo "   python3 scripts/test_app.py"
    echo ""
    echo "3. Khởi động dịch vụ:"
    echo "   ./scripts/start_service.sh"
    echo ""
    echo "4. Hoặc chạy thủ công:"
    echo "   source .venv/bin/activate"
    echo "   uvicorn src.main:app --host 0.0.0.0 --port 8000"
    echo ""
    echo "📖 Xem README.md để biết thêm chi tiết"
    echo "🌐 API sẽ chạy tại: http://localhost:8000"
    echo "📚 API docs: http://localhost:8000/docs"
    echo ""
    echo "⚠️  Lưu ý:"
    echo "- Nếu LED không sáng, chạy với sudo: sudo python3 scripts/test_led_simple.py"
    echo "- Kiểm tra kết nối phần cứng trong tài liệu KET_NOI_HARDWARE.md"
    echo "- Điều chỉnh cấu hình trong config/settings.yaml nếu cần"
}

run_auto_mode() {
    echo "🚀 Bắt đầu cài đặt LED Announcer Service..."
    require_non_root
    check_internet
    setup_system_packages
    install_rgb_led_matrix
    setup_python_env
    check_font
    run_tests
    print_next_steps
}

case "$MODE" in
    --auto)
        run_auto_mode
        ;;
    --manual)
        show_manual_steps
        ;;
    --help|-h)
        show_usage
        ;;
    *)
        echo "❌ Tùy chọn không hợp lệ: $MODE"
        show_usage
        exit 1
        ;;
esac
