#!/usr/bin/env python3
"""
Test vị trí text - tìm vị trí chính xác để hiển thị text ở giữa màn hình
Chạy với: sudo .venv/bin/python3 scripts/test_position.py
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import time

print("="*70)
print("TEST VỊ TRÍ TEXT - TÌM VỊ TRÍ CHÍNH XÁC")
print("="*70)
print()

# Cấu hình - 1 module 32x64
rows = 32
cols = 64
chain_length = 1
parallel = 1

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
    
    # Load font
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
    
    total_rows = rows * parallel
    total_cols = cols * chain_length
    
    print(f"Kích thước màn hình: {total_rows}x{total_cols}")
    print(f"Font height: {font_height}")
    print()
    
    print("="*70)
    print("TEST 1: Vẽ đường viền để xác định vị trí")
    print("="*70)
    print("→ Quan sát đường viền để xác định vị trí màn hình")
    print()
    canvas = matrix.CreateFrameCanvas()
    canvas.Clear()
    # Vẽ đường viền
    for x in range(total_cols):
        canvas.SetPixel(x, 0, 255, 0, 0)  # Đỏ - trên
        canvas.SetPixel(x, total_rows-1, 0, 255, 0)  # Xanh lá - dưới
    for y in range(total_rows):
        canvas.SetPixel(0, y, 0, 0, 255)  # Xanh dương - trái
        canvas.SetPixel(total_cols-1, y, 255, 255, 0)  # Vàng - phải
    # Vẽ đường giữa
    for x in range(total_cols):
        canvas.SetPixel(x, total_rows // 2, 255, 255, 255)  # Trắng - giữa ngang
    for y in range(total_rows):
        canvas.SetPixel(total_cols // 2, y, 255, 255, 255)  # Trắng - giữa dọc
    matrix.SwapOnVSync(canvas)
    time.sleep(5)
    print("✓ Đã vẽ đường viền\n")
    
    print("="*70)
    print("TEST 2: Text ở các vị trí Y khác nhau")
    print("="*70)
    print("→ Quan sát text ở vị trí nào nằm giữa màn hình")
    print()
    
    # Test nhiều vị trí Y
    test_positions = [
        (font_height, "Top"),
        (total_rows // 4, "1/4 từ trên"),
        (total_rows // 2 - font_height // 2, "Giữa (theo cách cũ)"),
        (total_rows // 2, "Giữa chính xác"),
        (total_rows // 2 + font_height // 2, "Giữa + font_height/2"),
        (total_rows // 2 + font_height // 2 - 1, "Giữa + font_height/2 - 1"),
        (total_rows // 2 + font_height // 2 - 2, "Giữa + font_height/2 - 2"),
        (total_rows * 3 // 4, "3/4 từ trên"),
        (total_rows - 5, "Gần dưới"),
    ]
    
    for y_pos, desc in test_positions:
        print(f"  Vị trí Y = {y_pos} ({desc})")
        canvas.Clear()
        text = "CENTER"
        text_length = graphics.DrawText(canvas, font, 0, y_pos, white, text)
        start_x = max((total_cols - text_length) // 2, 0)
        canvas.Clear()
        graphics.DrawText(canvas, font, start_x, y_pos, white, text)
        matrix.SwapOnVSync(canvas)
        print(f"    Text length: {text_length}, Start X: {start_x}")
        time.sleep(3)
    
    print("✓ Đã test các vị trí\n")
    
    print("="*70)
    print("TEST 3: Text đơn giản ở vị trí được đề xuất")
    print("="*70)
    print("→ Vị trí này có đúng không?")
    print()
    
    # Vị trí được đề xuất: giữa màn hình
    baseline = total_rows // 2 + font_height // 2
    text = "HELLO"
    text_length = graphics.DrawText(canvas, font, 0, baseline, red, text)
    start_x = max((total_cols - text_length) // 2, 0)
    canvas.Clear()
    graphics.DrawText(canvas, font, start_x, baseline, red, text)
    print(f"  Baseline: {baseline} (total_rows={total_rows}, font_height={font_height})")
    print(f"  Start X: {start_x} (total_cols={total_cols}, text_length={text_length})")
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
    print("Vị trí nào trong TEST 2 làm text nằm chính giữa màn hình?")
    print("Cho biết vị trí Y để cập nhật code.")
    print()
    
except Exception as e:
    print(f"\n✗ Lỗi: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

