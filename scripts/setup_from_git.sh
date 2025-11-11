#!/bin/bash

# Script cài đặt tự động LED Announcer từ GitHub
# Dành cho Raspberry Pi OS

set -e  # Dừng script nếu có lỗi

echo "🚀 Bắt đầu cài đặt LED Announcer Service..."

# Kiểm tra quyền root
if [[ $EUID -eq 0 ]]; then
   echo "❌ Đừng chạy script này với quyền root (sudo)"
   echo "👉 Chạy với user thường: ./scripts/setup_from_git.sh"
   exit 1
fi

# Kiểm tra kết nối internet
echo "🌐 Kiểm tra kết nối internet..."
if ! ping -c 1 google.com &> /dev/null; then
    echo "❌ Không có kết nối internet. Vui lòng kiểm tra lại."
    exit 1
fi

# Update hệ thống
echo "📦 Updating system packages..."
sudo apt update
sudo apt upgrade -y

# Cài đặt các package cần thiết
echo "🔧 Installing required packages..."
sudo apt install -y python3-pip python3-venv build-essential python3-dev git mpg123 curl cython3 cython3

# Chạy setup script
echo "🔧 Running setup script..."
chmod +x scripts/setup_from_git.sh
./scripts/setup_from_git.sh

# Kiểm tra và cài đặt rpi-rgb-led-matrix
echo "🔌 Installing rpi-rgb-led-matrix library..."
if [ ! -d "$HOME/rpi-rgb-led-matrix" ]; then
    echo "Cloning rpi-rgb-led-matrix..."
    cd ~
    git clone https://github.com/hzeller/rpi-rgb-led-matrix.git
    cd rpi-rgb-led-matrix
else
    echo "rpi-rgb-led-matrix already exists, updating..."
    cd ~/rpi-rgb-led-matrix
    git pull
fi

# Build và cài đặt
echo "Building and installing rpi-rgb-led-matrix..."
make build-python
sudo make install-python

# Quay lại thư mục dự án
cd ~/led_announcer

# Tạo virtual environment
echo "🐍 Creating Python virtual environment..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

# Kích hoạt virtual environment và cài đặt dependencies
echo "📚 Installing Python dependencies..."
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Kiểm tra font
echo "🔤 Checking font availability..."
FONT_PATH="/home/pi/rpi-rgb-led-matrix/fonts/10x20.bdf"
if [ ! -f "$FONT_PATH" ]; then
    echo "⚠️  Font not found at $FONT_PATH"
    echo "🔍 Creating fonts directory and downloading basic font..."
    sudo mkdir -p /home/pi/rpi-rgb-led-matrix/fonts/
    
    # Tạo font đơn giản nếu không có
    if [ ! -f "/home/pi/rpi-rgb-led-matrix/fonts/10x20.bdf" ]; then
        echo "Font sẽ được tạo tự động khi chạy test lần đầu"
    fi
fi

# Cấu hình permissions
echo "🔐 Setting up permissions..."
chmod +x scripts/*.sh
chmod +x scripts/*.py

# Test cài đặt
echo "🧪 Testing installation..."
source .venv/bin/activate

# Test import các thư viện
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

# Test rpi-rgb-led-matrix
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
