#!/usr/bin/env python3
"""
Test căn giữa text - kiểm tra text có nằm chính giữa màn hình không
Chạy với: sudo .venv/bin/python3 scripts/test_center.py
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import time

print("="*70)
print("TEST CĂN GIỮA TEXT")
print("="*70)
print()

# Cấu hình
rows = 32
cols = 64
chain_length = 1
parallel = 1

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
    matrix = RGBMatrix(options=options)
    print("✓ LED Matrix khởi tạo thành công!\n")
    
    font_path = Path("/home/loaled/rpi-rgb-led-matrix/fonts/6x10.bdf")
    font = graphics.Font()
    font.LoadFont(str(font_path))
    font_height = font.height
    
    total_rows = rows * parallel
    total_cols = cols * chain_length
    
    print(f"Màn hình: {total_rows}x{total_cols}")
    print(f"Font height: {font_height}")
    print()
    
    white = graphics.Color(255, 255, 255)
    red = graphics.Color(255, 0, 0)
    green = graphics.Color(0, 255, 0)
    blue = graphics.Color(0, 0, 255)
    
    print("="*70)
    print("TEST 1: Vẽ điểm giữa màn hình")
    print("="*70)
    print("→ Bạn có thấy điểm sáng ở chính giữa màn hình không?")
    print()
    canvas = matrix.CreateFrameCanvas()
    canvas.Clear()
    center_x = total_cols // 2
    center_y = total_rows // 2
    # Vẽ điểm giữa
    for dx in range(-2, 3):
        for dy in range(-2, 3):
            if 0 <= center_x + dx < total_cols and 0 <= center_y + dy < total_rows:
                canvas.SetPixel(center_x + dx, center_y + dy, 255, 255, 255)
    matrix.SwapOnVSync(canvas)
    time.sleep(3)
    print(f"  Điểm giữa: ({center_x}, {center_y})")
    print("✓ Đã vẽ điểm giữa\n")
    
    print("="*70)
    print("TEST 2: Text 'HELLO' căn giữa")
    print("="*70)
    print("→ Text có nằm chính giữa màn hình không?")
    print()
    canvas.Clear()
    baseline = total_rows // 2 + font_height // 2
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
    baseline = total_rows // 2 + font_height // 2
    text = "HELLO"
    canvas.Clear()
    text_length = graphics.DrawText(canvas, font, 0, baseline, white, text)
    start_x = max((total_cols - text_length) // 2, 0)
    canvas.Clear()
    graphics.DrawText(canvas, font, start_x, baseline, white, text)
    # Vẽ điểm đỏ ở giữa text
    text_center_x = start_x + text_length // 2
    text_center_y = baseline - font_height // 2
    canvas.SetPixel(text_center_x, text_center_y, 255, 0, 0)
    canvas.SetPixel(text_center_x - 1, text_center_y, 255, 0, 0)
    canvas.SetPixel(text_center_x + 1, text_center_y, 255, 0, 0)
    canvas.SetPixel(text_center_x, text_center_y - 1, 255, 0, 0)
    canvas.SetPixel(text_center_x, text_center_y + 1, 255, 0, 0)
    # Vẽ điểm xanh ở giữa màn hình
    canvas.SetPixel(total_cols // 2, total_rows // 2, 0, 255, 0)
    matrix.SwapOnVSync(canvas)
    print(f"  Giữa text: ({text_center_x}, {text_center_y})")
    print(f"  Giữa màn hình: ({total_cols // 2}, {total_rows // 2})")
    time.sleep(5)
    print("✓ Đã hiển thị\n")
    
    print("="*70)
    print("TEST 4: Text ngắn 'HI'")
    print("="*70)
    print("→ Text ngắn có nằm giữa không?")
    print()
    canvas.Clear()
    baseline = total_rows // 2 + font_height // 2
    text = "HI"
    text_length = graphics.DrawText(canvas, font, 0, baseline, white, text)
    start_x = max((total_cols - text_length) // 2, 0)
    canvas.Clear()
    graphics.DrawText(canvas, font, start_x, baseline, white, text)
    # Vẽ điểm đỏ ở giữa text
    text_center_x = start_x + text_length // 2
    text_center_y = baseline - font_height // 2
    canvas.SetPixel(text_center_x, text_center_y, 255, 0, 0)
    # Vẽ điểm xanh ở giữa màn hình
    canvas.SetPixel(total_cols // 2, total_rows // 2, 0, 255, 0)
    matrix.SwapOnVSync(canvas)
    print(f"  Text length: {text_length}, Start X: {start_x}")
    print(f"  Giữa text X: {text_center_x}, Giữa màn hình X: {total_cols // 2}")
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

