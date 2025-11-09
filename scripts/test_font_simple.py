#!/usr/bin/env python3
"""
Test font và hiển thị text với cấu hình đơn giản - 32x64, chain=1, parallel=1
Chạy với: sudo .venv/bin/python3 scripts/test_font_simple.py
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import time

print("="*70)
print("TEST FONT VÀ HIỂN THỊ TEXT - CẤU HÌNH ĐƠN GIẢN")
print("="*70)
print()

# Cấu hình đơn giản - 1 module 32x64
rows = 32
cols = 64
chain_length = 1  # Chỉ 1 module
parallel = 1      # Chỉ 1 panel

print(f"Cấu hình:")
print(f"  - Module: {rows}x{cols}")
print(f"  - Chain length: {chain_length}")
print(f"  - Parallel: {parallel}")
print(f"  - Tổng kích thước: {rows * parallel}x{cols * chain_length}")
print()

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
    
    # Test với nhiều font khác nhau
    fonts_to_test = [
        ("6x10.bdf", "Font 6x10 (nhỏ)"),
        ("7x13.bdf", "Font 7x13 (vừa)"),
        ("10x20.bdf", "Font 10x20 (lớn)"),
    ]
    
    white = graphics.Color(255, 255, 255)
    red = graphics.Color(255, 0, 0)
    
    for font_file, font_desc in fonts_to_test:
        font_path = Path(f"/home/loaled/rpi-rgb-led-matrix/fonts/{font_file}")
        
        if not font_path.exists():
            print(f"✗ Font không tìm thấy: {font_path}")
            continue
        
        print("="*70)
        print(f"TEST VỚI {font_desc}")
        print("="*70)
        print()
        
        font = graphics.Font()
        font.LoadFont(str(font_path))
        font_height = font.height
        
        print(f"Font: {font_file}, Height: {font_height} pixels")
        print(f"Màn hình: {rows}x{cols}")
        print()
        
        # Test 1: Hiển thị text ở góc trên trái
        print(f"TEST 1: Text ở góc trên trái (0, {font_height})")
        print("→ Bạn có thấy text 'TEST' ở góc trên trái không?")
        canvas = matrix.CreateFrameCanvas()
        canvas.Clear()
        graphics.DrawText(canvas, font, 0, font_height, white, "TEST")
        matrix.SwapOnVSync(canvas)
        time.sleep(5)
        print("✓ Đã hiển thị\n")
        
        # Test 2: Hiển thị text ở giữa màn hình
        print(f"TEST 2: Text ở giữa màn hình")
        print("→ Bạn có thấy text 'CENTER' ở giữa màn hình không?")
        canvas.Clear()
        baseline = rows // 2 + font_height // 2 - 2
        text = "CENTER"
        text_length = graphics.DrawText(canvas, font, 0, baseline, white, text)
        start_x = max((cols - text_length) // 2, 0)
        canvas.Clear()
        graphics.DrawText(canvas, font, start_x, baseline, white, text)
        print(f"  Baseline: {baseline}, Text length: {text_length}, Start X: {start_x}")
        matrix.SwapOnVSync(canvas)
        time.sleep(5)
        print("✓ Đã hiển thị\n")
        
        # Test 3: Hiển thị text đơn giản
        print(f"TEST 3: Text đơn giản 'HELLO'")
        print("→ Bạn có thấy text 'HELLO' không?")
        canvas.Clear()
        baseline = rows // 2 + font_height // 2 - 2
        text = "HELLO"
        text_length = graphics.DrawText(canvas, font, 0, baseline, red, text)
        start_x = max((cols - text_length) // 2, 0)
        canvas.Clear()
        graphics.DrawText(canvas, font, start_x, baseline, red, text)
        matrix.SwapOnVSync(canvas)
        time.sleep(5)
        print("✓ Đã hiển thị\n")
        
        # Test 4: Hiển thị từng ký tự
        print(f"TEST 4: Hiển thị từng ký tự")
        print("→ Quan sát từng chữ cái")
        for char in "ABCDEFG":
            canvas.Clear()
            baseline = rows // 2 + font_height // 2 - 2
            text_length = graphics.DrawText(canvas, font, 0, baseline, white, char)
            start_x = max((cols - text_length) // 2, 0)
            canvas.Clear()
            graphics.DrawText(canvas, font, start_x, baseline, white, char)
            matrix.SwapOnVSync(canvas)
            print(f"  Đã hiển thị: {char}")
            time.sleep(2)
        print("✓ Đã hiển thị tất cả ký tự\n")
        
        print("-" * 70)
        print()
    
    # Xóa
    print("Đang xóa màn hình...")
    matrix.Clear()
    print("✓ Hoàn tất!\n")
    
    print("="*70)
    print("KẾT QUẢ")
    print("="*70)
    print()
    print("Bạn có thấy text với font nào không?")
    print("Cho biết font nào hoạt động tốt nhất.")
    print()
    
except Exception as e:
    print(f"\n✗ Lỗi: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

