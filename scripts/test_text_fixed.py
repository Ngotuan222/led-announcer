#!/usr/bin/env python3
"""
Test hiển thị text với cấu hình đúng - chain_length=4, parallel=2
Chạy với: sudo .venv/bin/python3 scripts/test_text_fixed.py
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import time

print("="*70)
print("TEST HIỂN THỊ TEXT - VỚI CẤU HÌNH ĐÚNG")
print("="*70)
print()

# Cấu hình từ settings.yaml
rows = 32
cols = 64
chain_length = 4  # 4 module nối tiếp
parallel = 2      # 2 panel song song
# Tổng kích thước: 64*4 = 256 cột, 32*2 = 64 hàng

print(f"Cấu hình:")
print(f"  - Module: {rows}x{cols}")
print(f"  - Chain length: {chain_length} (tổng chiều ngang: {cols * chain_length})")
print(f"  - Parallel: {parallel} (tổng chiều dọc: {rows * parallel})")
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
    
    # Tính toán kích thước thực tế
    total_rows = rows * parallel
    total_cols = cols * chain_length
    
    print(f"Kích thước màn hình thực tế: {total_rows}x{total_cols}")
    print(f"Font height: {font_height}")
    print()
    
    # Tạo màu
    white = graphics.Color(255, 255, 255)
    red = graphics.Color(255, 0, 0)
    
    print("="*70)
    print("TEST 1: Hiển thị màu trắng toàn màn hình (3 giây)")
    print("="*70)
    print("→ Bạn có thấy màn hình sáng trắng không?")
    print()
    canvas = matrix.CreateFrameCanvas()
    canvas.Fill(255, 255, 255)
    matrix.SwapOnVSync(canvas)
    time.sleep(3)
    print("✓ Đã hiển thị màu trắng\n")
    
    print("="*70)
    print("TEST 2: Hiển thị text ở góc trên trái")
    print("="*70)
    print("→ Bạn có thấy text 'TEST' ở góc trên trái không?")
    print()
    canvas.Clear()
    # Vẽ ở vị trí (10, font_height) - góc trên trái
    graphics.DrawText(canvas, font, 10, font_height, white, "TEST")
    matrix.SwapOnVSync(canvas)
    time.sleep(5)
    print("✓ Đã hiển thị\n")
    
    print("="*70)
    print("TEST 3: Hiển thị text ở giữa màn hình (theo total_rows)")
    print("="*70)
    print("→ Bạn có thấy text 'CENTER' ở giữa màn hình không?")
    print()
    canvas.Clear()
    # Tính baseline dựa trên total_rows
    baseline = total_rows // 2 + font_height // 2 - 2
    text = "CENTER"
    text_length = graphics.DrawText(canvas, font, 0, baseline, white, text)
    start_x = max((total_cols - text_length) // 2, 0)
    canvas.Clear()
    graphics.DrawText(canvas, font, start_x, baseline, white, text)
    print(f"  Total rows: {total_rows}, Baseline: {baseline}")
    print(f"  Total cols: {total_cols}, Text length: {text_length}, Start X: {start_x}")
    matrix.SwapOnVSync(canvas)
    time.sleep(5)
    print("✓ Đã hiển thị\n")
    
    print("="*70)
    print("TEST 4: Hiển thị text ở giữa màn hình (theo rows)")
    print("="*70)
    print("→ Bạn có thấy text 'MIDDLE' ở giữa màn hình không?")
    print()
    canvas.Clear()
    # Tính baseline dựa trên rows (32)
    baseline = rows // 2 + font_height // 2 - 2
    text = "MIDDLE"
    text_length = graphics.DrawText(canvas, font, 0, baseline, white, text)
    start_x = max((cols - text_length) // 2, 0)
    canvas.Clear()
    graphics.DrawText(canvas, font, start_x, baseline, white, text)
    print(f"  Rows: {rows}, Baseline: {baseline}")
    print(f"  Cols: {cols}, Text length: {text_length}, Start X: {start_x}")
    matrix.SwapOnVSync(canvas)
    time.sleep(5)
    print("✓ Đã hiển thị\n")
    
    print("="*70)
    print("TEST 5: Thử nhiều vị trí Y khác nhau")
    print("="*70)
    print("→ Quan sát text 'Y=XX' ở các vị trí khác nhau")
    print()
    
    for y_pos in [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]:
        print(f"  Vị trí Y = {y_pos}")
        canvas.Clear()
        graphics.DrawText(canvas, font, 10, y_pos, white, f"Y={y_pos}")
        matrix.SwapOnVSync(canvas)
        time.sleep(2)
    
    print("✓ Đã test các vị trí\n")
    
    print("="*70)
    print("TEST 6: Hiển thị text dài")
    print("="*70)
    print("→ Bạn có thấy text 'HELLO WORLD' không?")
    print()
    canvas.Clear()
    baseline = rows // 2 + font_height // 2 - 2
    text = "HELLO WORLD"
    text_length = graphics.DrawText(canvas, font, 0, baseline, red, text)
    start_x = max((total_cols - text_length) // 2, 0)
    canvas.Clear()
    graphics.DrawText(canvas, font, start_x, baseline, red, text)
    print(f"  Text length: {text_length}, Start X: {start_x}")
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
    print("Bạn có thấy text trong test nào không?")
    print("Cho biết test nào hoạt động để cập nhật code.")
    print()
    
except Exception as e:
    print(f"\n✗ Lỗi: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

