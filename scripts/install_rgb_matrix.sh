#!/usr/bin/env bash
# Script cài đặt rpi-rgb-led-matrix và Python bindings

set -euo pipefail

echo "=== Cài đặt rpi-rgb-led-matrix ==="
echo ""

# Kiểm tra đang chạy trên Raspberry Pi
if [ ! -f /proc/device-tree/model ]; then
    echo "⚠️  Cảnh báo: Không phát hiện Raspberry Pi"
    echo "   Thư viện này chỉ hoạt động trên Raspberry Pi"
    read -p "   Tiếp tục? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Lưu PROJECT_ROOT trước khi cd
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Thư mục cài đặt
INSTALL_DIR="$HOME/rpi-rgb-led-matrix"
REPO_URL="https://github.com/hzeller/rpi-rgb-led-matrix.git"

# Kiểm tra dependencies hệ thống
echo "1. Kiểm tra dependencies hệ thống..."
REQUIRED_PKGS=(
    "build-essential"
    "git"
    "python3-dev"
    "libgraphicsmagick++-dev"
    "libwebp-dev"
    "make"
    "cmake"
    "cython3"
)

MISSING_PKGS=()
for pkg in "${REQUIRED_PKGS[@]}"; do
    if ! dpkg -l | grep -q "^ii  $pkg "; then
        MISSING_PKGS+=("$pkg")
    fi
done

if [ ${#MISSING_PKGS[@]} -gt 0 ]; then
    echo "   → Cần cài đặt: ${MISSING_PKGS[*]}"
    echo "   → Đang cài đặt..."
    sudo apt-get update
    sudo apt-get install -y "${MISSING_PKGS[@]}"
else
    echo "   ✓ Tất cả dependencies đã có"
fi

# Clone repository
echo ""
echo "2. Clone repository rpi-rgb-led-matrix..."
if [ -d "$INSTALL_DIR" ]; then
    echo "   → Thư mục đã tồn tại, đang cập nhật..."
    cd "$INSTALL_DIR"
    git pull
else
    echo "   → Đang clone từ GitHub..."
    cd "$HOME"
    git clone "$REPO_URL"
    cd "$INSTALL_DIR"
fi

# Build thư viện C++
echo ""
echo "3. Build thư viện C++..."
make clean || true
make -j$(nproc)
echo "   ✓ Build C++ library thành công"

# Cài đặt Python bindings
echo ""
echo "4. Cài đặt Python bindings..."

# Kiểm tra virtual environment
VENV_PYTHON=""

if [ -f "$PROJECT_ROOT/.venv/bin/activate" ]; then
    echo "   → Sử dụng virtual environment của dự án"
    source "$PROJECT_ROOT/.venv/bin/activate"
    VENV_PYTHON="$PROJECT_ROOT/.venv/bin/python3"
else
    echo "   → Sử dụng Python hệ thống"
    VENV_PYTHON="python3"
fi

cd "$INSTALL_DIR/bindings/python"

# Cài Cython vào virtualenv nếu cần
if [ -n "$VIRTUAL_ENV" ]; then
    echo "   → Cài đặt Cython vào virtualenv..."
    $VENV_PYTHON -m pip install Cython >/dev/null 2>&1 || true
fi

# Build Cython files
echo "   → Đang build Cython files..."
cd rgbmatrix
if [ -f "core.pyx" ] && [ ! -f "core.cpp" ]; then
    cython3 --cplus -o core.cpp core.pyx 2>/dev/null || $VENV_PYTHON -m Cython --cplus -o core.cpp core.pyx
fi
if [ -f "graphics.pyx" ] && [ ! -f "graphics.cpp" ]; then
    cython3 --cplus -o graphics.cpp graphics.pyx 2>/dev/null || $VENV_PYTHON -m Cython --cplus -o graphics.cpp graphics.pyx
fi
cd ..

# Build và cài đặt Python bindings
echo "   → Đang build Python bindings..."
$VENV_PYTHON setup.py build_ext --inplace

echo "   → Đang cài đặt vào Python..."
$VENV_PYTHON setup.py install

# Kiểm tra cài đặt
echo ""
echo "5. Kiểm tra cài đặt..."
if $VENV_PYTHON -c "from rgbmatrix import RGBMatrix; print('✓ OK')" 2>/dev/null; then
    echo "   ✓ Thư viện rgbmatrix đã được cài đặt thành công!"
else
    echo "   ✗ Vẫn chưa thể import, thử với sudo..."
    if sudo $VENV_PYTHON -c "from rgbmatrix import RGBMatrix; print('✓ OK')" 2>/dev/null; then
        echo "   ✓ Thư viện hoạt động với sudo"
        echo "   → Có thể cần chạy ứng dụng với sudo hoặc cấu hình quyền GPIO"
    else
        echo "   ✗ Có vấn đề với cài đặt"
        echo "   → Kiểm tra lại log phía trên"
        exit 1
    fi
fi

echo ""
echo "=== Hoàn tất cài đặt ==="
echo ""
echo "Để test, chạy:"
echo "  cd $PROJECT_ROOT"
echo "  ./scripts/test_led_connection.sh"
echo ""
echo "Lưu ý:"
echo "  - Nếu gặp lỗi GPIO, có thể cần chạy với sudo"
echo "  - Hoặc thêm user vào group gpio: sudo usermod -a -G gpio \$USER"

