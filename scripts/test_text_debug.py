#!/usr/bin/env python3
"""
Test và debug hiển thị text - kiểm tra font, vị trí, màu sắc
Chạy với: sudo .venv/bin/python3 scripts/test_text_debug.py
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.config import load_config
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import time

print("="*70)
print("TEST VÀ DEBUG HIỂN THỊ TEXT")
print("="*70)
print()

# Load config
config = load_config()
led_config = config.led

print(f"Cấu hình:")
print(f"  - Kích thước: {led_config.rows}x{led_config.cols}")
print(f"  - Chain length: {led_config.chain_length}")
print(f"  - Parallel: {led_config.parallel}")
print(f"  - Font: {led_config.font_path}")
print(f"  - Text color: {led_config.text_color}")
print(f"  - Background color: {led_config.background_color}")
print()

# Tạo options
options = RGBMatrixOptions()
options.rows = led_config.rows
options.cols = led_config.cols
options.chain_length = led_config.chain_length
options.parallel = led_config.parallel
options.hardware_mapping = led_config.hardware_mapping
options.gpio_slowdown = led_config.gpio_slowdown
options.brightness = 100  # Độ sáng tối đa để dễ thấy
options.drop_privileges = False
if led_config.disable_hardware_pulse:
    options.disable_hardware_pulsing = True

try:
    print("Đang khởi tạo LED Matrix...")
    matrix = RGBMatrix(options=options)
    print("✓ LED Matrix khởi tạo thành công!\n")
    
    # Load font
    print("Đang load font...")
    font = graphics.Font()
    font_path = Path(led_config.font_path).expanduser().resolve()
    if not font_path.exists():
        print(f"✗ Font không tìm thấy: {font_path}")
        sys.exit(1)
    font.LoadFont(str(font_path))
    print(f"✓ Font đã load: {font_path}\n")
    
    # Lấy thông tin font
    font_height = font.height
    print(f"Font height: {font_height} pixels")
    print(f"Screen height: {led_config.rows} pixels")
    print(f"Screen width: {led_config.cols} pixels")
    print()
    
    # Tạo màu
    text_color = graphics.Color(*led_config.text_color)
    bg_color = graphics.Color(*led_config.background_color)
    
    print("="*70)
    print("TEST 1: Hiển thị text ở vị trí cố định (góc trên trái)")
    print("="*70)
    print("→ Bạn có thấy text 'TEST' ở góc trên trái không?")
    print()
    canvas = matrix.CreateFrameCanvas()
    canvas.Clear()
    # Vẽ text ở vị trí (10, font_height) - góc trên trái
    graphics.DrawText(canvas, font, 10, font_height, text_color, "TEST")
    matrix.SwapOnVSync(canvas)
    time.sleep(5)
    print("✓ Đã hiển thị\n")
    
    print("="*70)
    print("TEST 2: Hiển thị text ở giữa màn hình (theo code hiện tại)")
    print("="*70)
    print("→ Bạn có thấy text 'CENTER' ở giữa màn hình không?")
    print()
    canvas.Clear()
    baseline = led_config.rows // 2
    text = "CENTER"
    text_length = graphics.DrawText(canvas, font, 0, baseline, text_color, text)
    start_x = max((led_config.cols - text_length) // 2, 0)
    canvas.Clear()
    graphics.DrawText(canvas, font, start_x, baseline, text_color, text)
    print(f"  Baseline: {baseline}, Text length: {text_length}, Start X: {start_x}")
    matrix.SwapOnVSync(canvas)
    time.sleep(5)
    print("✓ Đã hiển thị\n")
    
    print("="*70)
    print("TEST 3: Hiển thị text ở giữa màn hình (điều chỉnh)")
    print("="*70)
    print("→ Bạn có thấy text 'MIDDLE' ở giữa màn hình không?")
    print()
    canvas.Clear()
    # Điều chỉnh baseline: rows // 2 + font_height // 2 - 2
    baseline = led_config.rows // 2 + font_height // 2 - 2
    text = "MIDDLE"
    text_length = graphics.DrawText(canvas, font, 0, baseline, text_color, text)
    start_x = max((led_config.cols - text_length) // 2, 0)
    canvas.Clear()
    graphics.DrawText(canvas, font, start_x, baseline, text_color, text)
    print(f"  Baseline (adjusted): {baseline}, Text length: {text_length}, Start X: {start_x}")
    matrix.SwapOnVSync(canvas)
    time.sleep(5)
    print("✓ Đã hiển thị\n")
    
    print("="*70)
    print("TEST 4: Hiển thị text với màu sáng (đỏ)")
    print("="*70)
    print("→ Bạn có thấy text 'RED' màu đỏ không?")
    print()
    canvas.Clear()
    red_color = graphics.Color(255, 0, 0)
    baseline = led_config.rows // 2 + font_height // 2 - 2
    text = "RED"
    text_length = graphics.DrawText(canvas, font, 0, baseline, red_color, text)
    start_x = max((led_config.cols - text_length) // 2, 0)
    canvas.Clear()
    graphics.DrawText(canvas, font, start_x, baseline, red_color, text)
    matrix.SwapOnVSync(canvas)
    time.sleep(5)
    print("✓ Đã hiển thị\n")
    
    print("="*70)
    print("TEST 5: Hiển thị text lớn hơn")
    print("="*70)
    print("→ Bạn có thấy text 'HELLO' không?")
    print()
    canvas.Clear()
    baseline = led_config.rows // 2 + font_height // 2 - 2
    text = "HELLO"
    text_length = graphics.DrawText(canvas, font, 0, baseline, text_color, text)
    start_x = max((led_config.cols - text_length) // 2, 0)
    canvas.Clear()
    graphics.DrawText(canvas, font, start_x, baseline, text_color, text)
    matrix.SwapOnVSync(canvas)
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
    print("Bạn có thấy text trong bất kỳ test nào không?")
    print("Nếu có, cho biết test nào hoạt động để cập nhật code.")
    print()
    
except Exception as e:
    print(f"\n✗ Lỗi: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

