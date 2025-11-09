#!/usr/bin/env python3
"""
Kiểm tra font có load đúng không và test hiển thị
Chạy với: sudo .venv/bin/python3 scripts/test_font_check.py
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import time

print("="*70)
print("KIỂM TRA FONT VÀ HIỂN THỊ TEXT")
print("="*70)
print()

# Cấu hình đơn giản - 1 module 32x64
rows = 32
cols = 64
chain_length = 1
parallel = 1

# Tạo options
options = RGBMatrixOptions()
options.rows = rows
options.cols = cols
options.chain_length = chain_length
options.parallel = parallel
options.hardware_mapping = "regular"
options.gpio_slowdown = 4
options.brightness = 100
options.drop_privileges = False
options.disable_hardware_pulsing = True

try:
    print("Đang khởi tạo LED Matrix...")
    matrix = RGBMatrix(options=options)
    print("✓ LED Matrix khởi tạo thành công!\n")
    
    # Test với font 6x10
    font_path = Path("/home/loaled/rpi-rgb-led-matrix/fonts/6x10.bdf")
    print(f"Đang load font: {font_path}")
    
    if not font_path.exists():
        print(f"✗ Font không tìm thấy: {font_path}")
        sys.exit(1)
    
    font = graphics.Font()
    font.LoadFont(str(font_path))
    font_height = font.height
    print(f"✓ Font đã load, height: {font_height} pixels\n")
    
    white = graphics.Color(255, 255, 255)
    red = graphics.Color(255, 0, 0)
    
    print("="*70)
    print("TEST 1: Hiển thị text 'TEST' ở góc trên trái")
    print("="*70)
    print("→ Bạn có thấy text 'TEST' đầy đủ không?")
    print()
    canvas = matrix.CreateFrameCanvas()
    canvas.Clear()
    graphics.DrawText(canvas, font, 0, font_height, white, "TEST")
    matrix.SwapOnVSync(canvas)
    time.sleep(5)
    print("✓ Đã hiển thị\n")
    
    print("="*70)
    print("TEST 2: Hiển thị text 'HELLO' ở giữa màn hình")
    print("="*70)
    print("→ Bạn có thấy text 'HELLO' đầy đủ không?")
    print()
    canvas.Clear()
    baseline = rows // 2 + font_height // 2 - 2
    text = "HELLO"
    text_length = graphics.DrawText(canvas, font, 0, baseline, white, text)
    start_x = max((cols - text_length) // 2, 0)
    canvas.Clear()
    graphics.DrawText(canvas, font, start_x, baseline, white, text)
    print(f"  Baseline: {baseline}, Text length: {text_length}, Start X: {start_x}")
    matrix.SwapOnVSync(canvas)
    time.sleep(5)
    print("✓ Đã hiển thị\n")
    
    print("="*70)
    print("TEST 3: Hiển thị từng ký tự để kiểm tra font")
    print("="*70)
    print("→ Quan sát từng chữ cái có hiển thị đúng không")
    print()
    for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
        canvas.Clear()
        baseline = rows // 2 + font_height // 2 - 2
        text_length = graphics.DrawText(canvas, font, 0, baseline, white, char)
        start_x = max((cols - text_length) // 2, 0)
        canvas.Clear()
        graphics.DrawText(canvas, font, start_x, baseline, white, char)
        matrix.SwapOnVSync(canvas)
        print(f"  Đã hiển thị: '{char}'")
        time.sleep(1)
    print("✓ Đã hiển thị tất cả ký tự\n")
    
    print("="*70)
    print("TEST 4: Hiển thị text tiếng Việt")
    print("="*70)
    print("→ Bạn có thấy text 'NGUYEN VAN A' không?")
    print()
    canvas.Clear()
    baseline = rows // 2 + font_height // 2 - 2
    text = "NGUYEN VAN A"
    text_length = graphics.DrawText(canvas, font, 0, baseline, red, text)
    start_x = max((cols - text_length) // 2, 0)
    canvas.Clear()
    graphics.DrawText(canvas, font, start_x, baseline, red, text)
    matrix.SwapOnVSync(canvas)
    time.sleep(5)
    print("✓ Đã hiển thị\n")
    
    # Xóa
    print("Đang xóa màn hình...")
    matrix.Clear()
    print("✓ Hoàn tất!\n")
    
except Exception as e:
    print(f"\n✗ Lỗi: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

