#!/usr/bin/env python3
"""
Test căn giữa text - kiểm tra text có nằm chính giữa màn hình không
Chạy với: sudo .venv/bin/python3 scripts/test_center.py
"""

import sys
from pathlib import Path
import yaml

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import time

print("="*70)
print("TEST CĂN GIỮA TEXT")
print("="*70)
print()

config_path = project_root / "config" / "settings.yaml"
with config_path.open("r", encoding="utf-8") as handle:
    config = yaml.safe_load(handle)

led_config = config.get("led", {})

# Cấu hình theo settings.yaml
rows = led_config.get("rows", 32)
cols = led_config.get("cols", 64)
chain_length = led_config.get("chain_length", 1)
parallel = led_config.get("parallel", 1)
gpio_slowdown = led_config.get("gpio_slowdown", 4)
brightness = led_config.get("brightness", 100)
hardware_mapping = led_config.get("hardware_mapping", "regular")
disable_hardware_pulse = led_config.get("disable_hardware_pulse", True)
scan_mode = led_config.get("scan_mode", 0)
font_path = Path(led_config.get("font_path", "/home/pi/rpi-rgb-led-matrix/fonts/10x20.bdf"))

options = RGBMatrixOptions()
options.rows = rows
options.cols = cols
options.chain_length = chain_length
options.parallel = parallel
options.hardware_mapping = hardware_mapping
options.gpio_slowdown = gpio_slowdown
options.brightness = brightness
options.drop_privileges = False
options.disable_hardware_pulsing = True  # Tránh conflict với sound module
if disable_hardware_pulse:
    options.disable_hardware_pulsing = True
options.scan_mode = scan_mode
options.multiplexing = led_config.get("multiplexing", 0)

try:
    matrix = RGBMatrix(options=options)
    print("✓ LED Matrix khởi tạo thành công!\n")
    
    font = graphics.Font()
    font.LoadFont(str(font_path))
    font_height = font.height
    
    total_rows = rows * parallel
    total_cols = cols * chain_length
    
    # Tính toán điểm trung tâm LOGIC cho màn hình LED 64x32 pixel
    # Chọn điểm xanh PHÍA TRÊN (gần giữa màn hình hơn) làm tâm logic
    center_x = 32  # Giữa của 64 pixel (0-63)
    center_y = 15  # Lấy điểm trên làm tâm
    
    print(f"  Màn hình: {total_rows}x{total_cols} (P4 Matrix)")
    print(f"  Font height: {font_height}")
    print(f"  Center pixel: ({center_x}, {center_y})")
    if total_cols % 2 == 0:
        print(f"  Note: Even number of columns, center is between pixels {center_x} and {center_x+1}")
    if total_rows % 2 == 0:
        print(f"  Note: Even number of rows, center is between pixels {center_y} and {center_y+1}")
    print()
    
    white = graphics.Color(255, 255, 255)
    red = graphics.Color(255, 0, 0)
    green = graphics.Color(0, 255, 0)
    blue = graphics.Color(0, 0, 255)
    
    print("="*70)
    print("TEST 1: Vẽ điểm giữa màn hình")
    print("="*70)
    print("→ Bạn có thấy điểm XANH duy nhất ở chính giữa màn hình không?")
    print()
    # Xóa toàn bộ matrix trước khi vẽ điểm
    matrix.Clear()
    canvas = matrix.CreateFrameCanvas()
    canvas.Clear()  # Xóa sạch canvas
    # Chỉ vẽ một điểm màu XANH LÁ CÂY duy nhất ở chính giữa
    canvas.SetPixel(center_x, center_y, 0, 255, 0)
    matrix.SwapOnVSync(canvas)
    time.sleep(5)
    print(f"  Điểm giữa: ({center_x}, {center_y})")
    print("✓ Đã vẽ điểm giữa\n")

    print("="*70)
    print("TEST 2: Text 'HELLO' căn giữa")
    print("="*70)
    print("→ Text có nằm chính giữa màn hình không?")
    print()
    canvas.Clear()
    # Căn baseline theo tâm logic: center_y ~ giữa chiều cao chữ
    baseline = center_y + font_height // 2
    text = "HELLO"
    text_length = graphics.DrawText(canvas, font, 0, baseline, white, text)
    start_x = max((total_cols - text_length) // 2, 0)
    canvas.Clear()
    graphics.DrawText(canvas, font, start_x, baseline, white, text)
    print(f"  Baseline: {baseline}")
    print(f"  Text length: {text_length}")
    print(f"  Start X: {start_x}")
    print(f"  End X: {start_x + text_length}")
    print(f"  Màn hình: 0 đến {total_cols-1}")
    print(f"  Giữa màn hình X: {total_cols // 2}")
    matrix.SwapOnVSync(canvas)
    time.sleep(5)
    print("✓ Đã hiển thị\n")
    
    print("="*70)
    print("TEST 3: Text với điểm đánh dấu giữa")
    print("="*70)
    print("→ Điểm đỏ có nằm ở giữa text không?")
    print()
    canvas.Clear()
    baseline = center_y + font_height // 2
    text = "HELLO"
    canvas.Clear()
    text_length = graphics.DrawText(canvas, font, 0, baseline, white, text)
    start_x = max((total_cols - text_length) // 2, 0)
    canvas.Clear()
    graphics.DrawText(canvas, font, start_x, baseline, white, text)
    # Vẽ điểm đỏ ở giữa text (điều chỉnh để khớp với center màn hình)
    text_center_x = start_x + text_length // 2
    text_center_y = baseline - font_height // 3
    
    # Điều chỉnh cho P4 matrix - căn chỉnh chính xác với center màn hình
    if total_cols % 2 == 0:
        text_center_x = center_x  # Force align with screen center
    if total_rows % 2 == 0:
        text_center_y = center_y  # Force align with screen center
    
    # Không vẽ điểm đỏ nữa - chỉ hiển thị text
    # canvas.SetPixel(text_center_x, text_center_y, 255, 0, 0)
    # canvas.SetPixel(text_center_x - 1, text_center_y, 255, 0, 0)
    # canvas.SetPixel(text_center_x + 1, text_center_y, 255, 0, 0)
    # canvas.SetPixel(text_center_x, text_center_y - 1, 255, 0, 0)
    # canvas.SetPixel(text_center_x, text_center_y + 1, 255, 0, 0)
    
    # Chỉ hiển thị text không có điểm đánh dấu
    canvas.Clear()
    baseline = center_y + font_height // 2
    text = "HELLO"
    text_length = graphics.DrawText(canvas, font, 0, baseline, white, text)
    start_x = max((total_cols - text_length) // 2, 0)
    canvas.Clear()
    graphics.DrawText(canvas, font, start_x, baseline, white, text)
    
    matrix.SwapOnVSync(canvas)
    print(f"  Giữa text: ({text_center_x}, {text_center_y})")
    print(f"  Giữa màn hình: ({center_x}, {center_y})")
    time.sleep(5)
    print("✓ Đã hiển thị\n")
    
    print("="*70)
    print("TEST 4: Text ngắn 'HI'")
    print("="*70)
    print("→ Text ngắn có nằm giữa không?")
    print()
    canvas.Clear()
    baseline = center_y + font_height // 2
    text = "HI"
    text_length = graphics.DrawText(canvas, font, 0, baseline, white, text)
    start_x = max((total_cols - text_length) // 2, 0)
    canvas.Clear()
    graphics.DrawText(canvas, font, start_x, baseline, white, text)
    # Vẽ điểm đỏ ở giữa text (điều chỉnh để khớp với center màn hình)
    text_center_x = start_x + text_length // 2
    text_center_y = baseline - font_height // 3
    
    # Điều chỉnh cho P4 matrix - căn chỉnh chính xác với center màn hình
    if total_cols % 2 == 0:
        text_center_x = center_x  # Force align with screen center
    if total_rows % 2 == 0:
        text_center_y = center_y  # Force align with screen center
    
    # Không vẽ điểm đỏ nữa - chỉ hiển thị text
    # canvas.SetPixel(text_center_x, text_center_y, 255, 0, 0)
    
    # Chỉ hiển thị text không có điểm đánh dấu
    canvas.Clear()
    baseline = center_y + font_height // 2
    text = "HI"
    text_length = graphics.DrawText(canvas, font, 0, baseline, white, text)
    start_x = max((total_cols - text_length) // 2, 0)
    canvas.Clear()
    graphics.DrawText(canvas, font, start_x, baseline, white, text)
    
    matrix.SwapOnVSync(canvas)
    print(f"  Text length: {text_length}, Start X: {start_x}")
    print(f"  Giữa text X: {text_center_x}, Giữa màn hình X: {center_x}")
    time.sleep(5)
    print("✓ Đã hiển thị\n")
    
    # Xóa
    print("Đang xóa màn hình...")
    matrix.Clear()
    print("✓ Hoàn tất!\n")
    
    print("="*70)
    print("KẾT QUẢ")
    print("="*70)
    print()
    print("Trong TEST 3 và TEST 4:")
    print("  - Điểm đỏ có trùng với điểm xanh không? (nếu có = text nằm giữa)")
    print("  - Text có bị cắt ở bên phải không?")
    print("  - Text có lệch về một phía không?")
    print()
    
except Exception as e:
    print(f"\n✗ Lỗi: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

