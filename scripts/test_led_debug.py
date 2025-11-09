#!/usr/bin/env python3
"""
Script debug để kiểm tra LED Matrix - thử nhiều cấu hình khác nhau
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from rgbmatrix import RGBMatrix, RGBMatrixOptions
import time

print("=" * 60)
print("KIỂM TRA LED MATRIX - DEBUG MODE")
print("=" * 60)

# Danh sách các cấu hình để thử
configs_to_try = [
    {
        "name": "Cấu hình 1: 32x64, chain=1, parallel=1",
        "rows": 32,
        "cols": 64,
        "chain": 1,
        "parallel": 1,
    },
    {
        "name": "Cấu hình 2: 32x64, chain=2, parallel=1",
        "rows": 32,
        "cols": 64,
        "chain": 2,
        "parallel": 1,
    },
    {
        "name": "Cấu hình 3: 32x64, chain=4, parallel=1",
        "rows": 32,
        "cols": 64,
        "chain": 4,
        "parallel": 1,
    },
    {
        "name": "Cấu hình 4: 32x64, chain=1, parallel=2",
        "rows": 32,
        "cols": 64,
        "chain": 1,
        "parallel": 2,
    },
    {
        "name": "Cấu hình 5: 32x64, chain=4, parallel=2",
        "rows": 32,
        "cols": 64,
        "chain": 4,
        "parallel": 2,
    },
]

for i, config in enumerate(configs_to_try, 1):
    print(f"\n{'='*60}")
    print(f"THỬ: {config['name']}")
    print(f"{'='*60}")
    
    try:
        options = RGBMatrixOptions()
        options.rows = config["rows"]
        options.cols = config["cols"]
        options.chain_length = config["chain"]
        options.parallel = config["parallel"]
        options.hardware_mapping = "regular"
        options.gpio_slowdown = 4
        options.brightness = 100
        options.disable_hardware_pulsing = True
        options.drop_privileges = False
        
        print(f"Đang khởi tạo...")
        matrix = RGBMatrix(options=options)
        print(f"✓ Khởi tạo thành công!")
        
        # Hiển thị màu trắng
        canvas = matrix.CreateFrameCanvas()
        canvas.Fill(255, 255, 255)
        matrix.SwapOnVSync(canvas)
        print(f"✓ Đã gửi MÀU TRẮNG - Bạn có thấy đèn sáng không?")
        print(f"  (Chờ 3 giây...)")
        time.sleep(3)
        
        # Hiển thị màu đỏ
        canvas.Fill(255, 0, 0)
        matrix.SwapOnVSync(canvas)
        print(f"✓ Đã gửi MÀU ĐỎ")
        time.sleep(2)
        
        matrix.Clear()
        print(f"✓ Cấu hình này hoạt động!")
        
        # Nếu thấy đèn sáng, dừng lại
        response = input("\n>>> Bạn có thấy đèn sáng với cấu hình này không? (y/n): ")
        if response.lower() == 'y':
            print(f"\n{'='*60}")
            print(f"THÀNH CÔNG! Cấu hình đúng là:")
            print(f"  - Rows: {config['rows']}")
            print(f"  - Cols: {config['cols']}")
            print(f"  - Chain length: {config['chain']}")
            print(f"  - Parallel: {config['parallel']}")
            print(f"{'='*60}")
            sys.exit(0)
        
    except Exception as e:
        print(f"✗ Lỗi với cấu hình này: {e}")
        continue

print(f"\n{'='*60}")
print("KHÔNG TÌM THẤY CẤU HÌNH PHÙ HỢP")
print(f"{'='*60}")
print("\nKiểm tra phần cứng:")
print("  1. ✓ Nguồn 5V đã được cấp cho module LED chưa?")
print("  2. ✓ Cáp IDC 16-pin đã cắm vào cổng DATA_IN chưa?")
print("  3. ✓ Cáp đã cắm đúng chiều chưa? (có rãnh định hướng)")
print("  4. ✓ Các chân GPIO đã kết nối đúng theo sơ đồ chưa?")
print("  5. ✓ Module LED có bật nguồn không?")
print("\nXem thêm: KIEM_TRA_PHAN_CUNG.md")

