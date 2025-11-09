#!/usr/bin/env python3
"""
Test hiển thị text đơn giản - debug từng bước
Chạy với: sudo .venv/bin/python3 scripts/test_text_simple.py
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import time

print("="*70)
print("TEST HIỂN THỊ TEXT - DEBUG TỪNG BƯỚC")
print("="*70)
print()

# Cấu hình
rows = 32
cols = 64
chain_length = 4
parallel = 2

print(f"Cấu hình:")
print(f"  - Kích thước: {rows}x{cols}")
print(f"  - Chain length: {chain_length}")
print(f"  - Parallel: {parallel}")
print()

# Tạo options
options = RGBMatrixOptions()
options.rows = rows
options.cols = cols
options.chain_length = chain_length
options.parallel = parallel
options.hardware_mapping = "regular"
options.gpio_slowdown = 4
options.brightness = 100  # Độ sáng tối đa
options.drop_privileges = False
options.disable_hardware_pulsing = True

try:
    print("Đang khởi tạo LED Matrix...")
    matrix = RGBMatrix(options=options)
    print("✓ LED Matrix khởi tạo thành công!\n")
    
    # Load font
    font_path = Path("/home/loaled/rpi-rgb-led-matrix/fonts/10x20.bdf")
    print(f"Đang load font: {font_path}")
    if not font_path.exists():
        print(f"✗ Font không tìm thấy: {font_path}")
        sys.exit(1)
    
    font = graphics.Font()
    font.LoadFont(str(font_path))
    font_height = font.height
    print(f"✓ Font đã load, height: {font_height} pixels\n")
    
    # Tạo màu
    white = graphics.Color(255, 255, 255)
    red = graphics.Color(255, 0, 0)
    green = graphics.Color(0, 255, 0)
    blue = graphics.Color(0, 0, 255)
    
    print("="*70)
    print("TEST 1: Hiển thị màu trắng toàn màn hình (5 giây)")
    print("="*70)
    print("→ Bạn có thấy màn hình sáng trắng không?")
    print()
    canvas = matrix.CreateFrameCanvas()
    canvas.Fill(255, 255, 255)
    matrix.SwapOnVSync(canvas)
    time.sleep(5)
    print("✓ Đã hiển thị màu trắng\n")
    
    print("="*70)
    print("TEST 2: Hiển thị text ở vị trí (0, font_height)")
    print("="*70)
    print("→ Bạn có thấy text 'TEST' ở góc trên trái không?")
    print()
    canvas.Clear()
    graphics.DrawText(canvas, font, 0, font_height, white, "TEST")
    matrix.SwapOnVSync(canvas)
    time.sleep(5)
    print("✓ Đã hiển thị\n")
    
    print("="*70)
    print("TEST 3: Hiển thị text ở vị trí (0, rows-5)")
    print("="*70)
    print("→ Bạn có thấy text 'BOTTOM' ở gần dưới màn hình không?")
    print()
    canvas.Clear()
    graphics.DrawText(canvas, font, 0, rows - 5, white, "BOTTOM")
    matrix.SwapOnVSync(canvas)
    time.sleep(5)
    print("✓ Đã hiển thị\n")
    
    print("="*70)
    print("TEST 4: Hiển thị text ở giữa màn hình (theo công thức mới)")
    print("="*70)
    print("→ Bạn có thấy text 'CENTER' ở giữa màn hình không?")
    print()
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
    
    print("="*70)
    print("TEST 5: Thử nhiều vị trí baseline khác nhau")
    print("="*70)
    print("→ Quan sát text 'POS' ở các vị trí khác nhau")
    print()
    
    for i, baseline in enumerate([10, 15, 20, 25, 30], 1):
        print(f"  Vị trí {i}: baseline = {baseline}")
        canvas.Clear()
        graphics.DrawText(canvas, font, 5, baseline, white, f"POS{i}")
        matrix.SwapOnVSync(canvas)
        time.sleep(3)
    
    print("✓ Đã test các vị trí\n")
    
    print("="*70)
    print("TEST 6: Hiển thị text với màu đỏ")
    print("="*70)
    print("→ Bạn có thấy text 'RED' màu đỏ không?")
    print()
    canvas.Clear()
    baseline = rows // 2 + font_height // 2 - 2
    text = "RED"
    text_length = graphics.DrawText(canvas, font, 0, baseline, red, text)
    start_x = max((cols - text_length) // 2, 0)
    canvas.Clear()
    graphics.DrawText(canvas, font, start_x, baseline, red, text)
    matrix.SwapOnVSync(canvas)
    time.sleep(5)
    print("✓ Đã hiển thị\n")
    
    print("="*70)
    print("TEST 7: Hiển thị text với nền màu")
    print("="*70)
    print("→ Bạn có thấy text 'BG' với nền xanh không?")
    print()
    canvas.Clear()
    # Vẽ nền xanh
    for y in range(rows):
        for x in range(cols):
            canvas.SetPixel(x, y, 0, 0, 255)
    baseline = rows // 2 + font_height // 2 - 2
    text = "BG"
    text_length = graphics.DrawText(canvas, font, 0, baseline, white, text)
    start_x = max((cols - text_length) // 2, 0)
    graphics.DrawText(canvas, font, start_x, baseline, white, text)
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
    print("Nếu có, cho biết test nào hoạt động.")
    print("Nếu không, có thể vấn đề là:")
    print("  1. Font không load được đúng cách")
    print("  2. Cấu hình rows/cols/chain/parallel không đúng")
    print("  3. Text bị cắt hoặc nằm ngoài màn hình")
    print()
    
except Exception as e:
    print(f"\n✗ Lỗi: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

