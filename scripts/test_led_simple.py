#!/usr/bin/env python3
"""
Script test đơn giản để kiểm tra LED Matrix
Chạy với: python3 scripts/test_led_simple.py
Hoặc: sudo .venv/bin/python3 scripts/test_led_simple.py (nếu cần quyền GPIO)
"""

import sys
import os
from pathlib import Path

# Tự động tìm Python từ venv nếu có
project_root = Path(__file__).parent.parent
venv_python = project_root / ".venv" / "bin" / "python3"

# Nếu đang chạy với sudo và venv python có sẵn, sử dụng venv python
if os.geteuid() == 0 and venv_python.exists():
    # Đang chạy với sudo, nhưng script đã được gọi với python3 hệ thống
    # Hướng dẫn user chạy lại với venv python
    if sys.executable != str(venv_python):
        print("⚠️  Đang chạy với sudo nhưng sử dụng Python hệ thống")
        print(f"   → Chạy lại với: sudo {venv_python} {sys.argv[0]}")
        print(f"   → Hoặc không cần sudo (user đã trong group gpio)")
        sys.exit(1)

# Thêm thư mục src vào path
sys.path.insert(0, str(project_root / "src"))

try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
    print("✓ Thư viện rgbmatrix OK")
except ImportError as e:
    print(f"✗ Không thể import rgbmatrix: {e}")
    print("→ Cần cài đặt rpi-rgb-led-matrix")
    sys.exit(1)

# Đọc cấu hình
config_path = project_root / "config" / "settings.yaml"
if not config_path.exists():
    print(f"✗ Không tìm thấy file cấu hình: {config_path}")
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
options.hardware_mapping = led_config.get("hardware_mapping", "adafruit-hat")
options.gpio_slowdown = led_config.get("gpio_slowdown", 4)
options.brightness = led_config.get("brightness", 70)
options.drop_privileges = False
# Tắt hardware pulse nếu không có root
if led_config.get("disable_hardware_pulse", True):
    options.disable_hardware_pulsing = True
    options.scan_mode = led_config.get("scan_mode", 0)

print(f"\nCấu hình LED Matrix:")
print(f"  - Kích thước: {options.rows}x{options.cols}")
print(f"  - Chain length: {options.chain_length}")
print(f"  - Parallel: {options.parallel}")
print(f"  - Hardware mapping: {options.hardware_mapping}")
print(f"  - GPIO slowdown: {options.gpio_slowdown}")
print(f"  - Brightness: {options.brightness}%")

try:
    print("\nĐang khởi tạo LED Matrix...")
    matrix = RGBMatrix(options=options)
    print("✓ LED Matrix khởi tạo thành công!")
    
    # Test 1: Hiển thị màn hình đen
    print("\nTest 1: Hiển thị màn hình đen...")
    canvas = matrix.CreateFrameCanvas()
    canvas.Clear()
    matrix.SwapOnVSync(canvas)
    import time
    time.sleep(2)
    print("✓ OK")
    
    # Test 2: Hiển thị màu đỏ
    print("\nTest 2: Hiển thị màu đỏ...")
    canvas.Clear()
    canvas.Fill(255, 0, 0)  # Đỏ
    matrix.SwapOnVSync(canvas)
    time.sleep(2)
    print("✓ OK")
    
    # Test 3: Hiển thị màu xanh lá
    print("\nTest 3: Hiển thị màu xanh lá...")
    canvas.Clear()
    canvas.Fill(0, 255, 0)  # Xanh lá
    matrix.SwapOnVSync(canvas)
    time.sleep(2)
    print("✓ OK")
    
    # Test 4: Hiển thị màu xanh dương
    print("\nTest 4: Hiển thị màu xanh dương...")
    canvas.Clear()
    canvas.Fill(0, 0, 255)  # Xanh dương
    matrix.SwapOnVSync(canvas)
    time.sleep(2)
    print("✓ OK")
    
    # Test 5: Hiển thị text
    print("\nTest 5: Hiển thị text...")
    try:
        font_path = led_config.get("font_path", "/home/pi/rpi-rgb-led-matrix/fonts/10x20.bdf")
        font = graphics.Font()
        font.LoadFont(font_path)
        
        canvas.Clear()
        text_color = graphics.Color(255, 255, 255)
        graphics.DrawText(canvas, font, 10, 64, text_color, "TEST")
        matrix.SwapOnVSync(canvas)
        time.sleep(3)
        print("✓ OK")
    except Exception as e:
        print(f"⚠ Không thể load font: {e}")
        print("  (Bỏ qua test text)")
    
    # Xóa màn hình
    print("\nĐang xóa màn hình...")
    matrix.Clear()
    print("✓ Hoàn tất!")
    print("\n=== Tất cả test đều thành công! ===")
    
except Exception as e:
    print(f"\n✗ Lỗi: {e}")
    import traceback
    traceback.print_exc()
    print("\nKiểm tra:")
    print("  1. Kết nối phần cứng (cáp IDC 16-pin)")
    print("  2. Nguồn điện 5V cho LED")
    print("  3. Cấu hình hardware_mapping")
    print("  4. Quyền truy cập GPIO (thử chạy với sudo)")
    sys.exit(1)

