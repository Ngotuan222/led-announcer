#!/usr/bin/env bash
# Script kiểm tra kết nối LED Matrix

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_PYTHON="$PROJECT_ROOT/.venv/bin/python3"

echo "=== Kiểm tra kết nối LED Matrix ==="
echo ""

# Kiểm tra venv
if [ ! -f "$VENV_PYTHON" ]; then
    echo "✗ Virtual environment chưa được tạo"
    echo "   Chạy: ./scripts/install_dependencies.sh"
    exit 1
fi

# Kiểm tra thư viện
echo "1. Kiểm tra thư viện rgbmatrix..."
if "$VENV_PYTHON" -c "from rgbmatrix import RGBMatrix" 2>/dev/null; then
    echo "   ✓ Thư viện rgbmatrix đã được cài đặt"
else
    echo "   ✗ Thư viện rgbmatrix chưa được cài đặt trong venv"
    echo ""
    echo "   → Cần cài đặt rpi-rgb-led-matrix"
    echo "   → Chạy script cài đặt:"
    echo "     ./scripts/install_rgb_matrix.sh"
    echo ""
    echo "   → Hoặc cài đặt thủ công từ:"
    echo "     https://github.com/hzeller/rpi-rgb-led-matrix"
    exit 1
fi

# Kiểm tra GPIO
echo ""
echo "2. Kiểm tra quyền truy cập GPIO..."
if [ -d "/sys/class/gpio" ]; then
    echo "   ✓ GPIO interface có sẵn"
else
    echo "   ✗ GPIO interface không tìm thấy"
fi

# Kiểm tra cấu hình
echo ""
echo "3. Kiểm tra file cấu hình..."
if [ -f "$PROJECT_ROOT/config/settings.yaml" ]; then
    echo "   ✓ File cấu hình tồn tại"
    echo "   → Đường dẫn: $PROJECT_ROOT/config/settings.yaml"
else
    echo "   ✗ File cấu hình không tìm thấy"
fi

# Thử khởi tạo LED Matrix
echo ""
echo "4. Thử khởi tạo LED Matrix..."
cd "$PROJECT_ROOT"

"$VENV_PYTHON" << EOF
import sys
from pathlib import Path

try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions
    
    # Đọc cấu hình
    config_path = Path("$PROJECT_ROOT/config/settings.yaml")
    if not config_path.exists():
        print("   ✗ File cấu hình không tìm thấy")
        sys.exit(1)
    
    import yaml
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    led_config = config.get("led", {})
    
    # Tạo options
    options = RGBMatrixOptions()
    options.rows = led_config.get("rows", 128)
    options.cols = led_config.get("cols", 256)
    options.chain_length = led_config.get("chain_length", 1)
    options.parallel = led_config.get("parallel", 1)
    options.hardware_mapping = led_config.get("hardware_mapping", "regular")
    options.gpio_slowdown = led_config.get("gpio_slowdown", 4)
    options.brightness = led_config.get("brightness", 70)
    options.drop_privileges = False
    # Tắt hardware pulse nếu không có root (theo config)
    if led_config.get("disable_hardware_pulse", True):
        options.disable_hardware_pulsing = True
    
    print(f"   → Cấu hình: {options.rows}x{options.cols}, chain={options.chain_length}, parallel={options.parallel}")
    print(f"   → Hardware mapping: {options.hardware_mapping}")
    print(f"   → GPIO slowdown: {options.gpio_slowdown}")
    
    # Thử khởi tạo
    try:
        matrix = RGBMatrix(options=options)
        print("   ✓ LED Matrix khởi tạo thành công!")
        print("   → Kết nối phần cứng OK")
        
        # Thử hiển thị một frame đen
        canvas = matrix.CreateFrameCanvas()
        canvas.Clear()
        matrix.SwapOnVSync(canvas)
        print("   ✓ Test hiển thị thành công!")
        
        # Giữ frame trong 1 giây
        import time
        time.sleep(1)
        
        matrix.Clear()
        print("   ✓ LED Matrix đã được xóa")
        
    except Exception as e:
        print(f"   ✗ Lỗi khởi tạo LED Matrix: {e}")
        print("   → Kiểm tra lại:")
        print("     - Kết nối phần cứng (cáp IDC 16-pin)")
        print("     - Nguồn điện 5V cho LED")
        print("     - Cấu hình hardware_mapping")
        print("     - Quyền truy cập GPIO (có thể cần sudo)")
        sys.exit(1)
        
except ImportError as e:
    print(f"   ✗ Không thể import rgbmatrix: {e}")
    print("   → Cần cài đặt rpi-rgb-led-matrix")
    print("   → Xem hướng dẫn: https://github.com/hzeller/rpi-rgb-led-matrix")
    sys.exit(1)
except Exception as e:
    print(f"   ✗ Lỗi: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
EOF

if [ $? -eq 0 ]; then
    echo ""
    echo "=== Kết quả: Kết nối LED Matrix hoạt động tốt! ==="
else
    echo ""
    echo "=== Kết quả: Có lỗi, vui lòng kiểm tra lại ==="
    exit 1
fi

