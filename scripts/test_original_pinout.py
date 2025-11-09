#!/usr/bin/env python3
"""
Test với sơ đồ chân ban đầu (có thể đúng với module LED của bạn)
Sơ đồ này dựa trên nhãn in trên PCB của module LED P4 (HUB-75E)
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from rgbmatrix import RGBMatrix, RGBMatrixOptions
import time

print("=" * 70)
print("TEST VỚI SƠ ĐỒ CHÂN BAN ĐẦU (theo PCB module)")
print("=" * 70)
print()
print("Sơ đồ chân ban đầu (có thể đúng với module LED của bạn):")
print()
print("| Chân IDC | Tín hiệu | GPIO | Pin vật lý |")
print("|----------|----------|------|------------|")
print("| 1        | R1       | 17   | 11         |")
print("| 2        | G1       | 18   | 12         |")
print("| 3        | B1       | 22   | 15         |")
print("| 5        | R2       | 23   | 16         |")
print("| 6        | G2       | 24   | 18         |")
print("| 7        | B2       | 25   | 22         |")
print("| 8        | E        | 19   | 35         |")
print("| 9        | A        | 26   | 37         |")
print("| 10       | B        | 27   | 13         |")
print("| 11       | C        | 5    | 29         |")
print("| 12       | D        | 6    | 31         |")
print("| 13       | CLK      | 21   | 40         |")
print("| 14       | LAT      | 20   | 38         |")
print("| 15       | OE       | 16   | 36         |")
print()

print("⚠️  LƯU Ý: Sơ đồ này KHÁC với mapping 'regular'")
print("   Nếu module LED của bạn có sơ đồ chân này, bạn cần")
print("   tạo custom hardware mapping hoặc sử dụng mapping khác.")
print()

print("=" * 70)
print("KIỂM TRA SƠ ĐỒ CHÂN TRÊN PCB CỦA MODULE LED")
print("=" * 70)
print()
print("Vui lòng kiểm tra:")
print("1. Xem sơ đồ chân IN TRÊN PCB của module LED")
print("   (thường in ở gần cổng IDC 16-pin)")
print()
print("2. So sánh với sơ đồ trên")
print()
print("3. Nếu sơ đồ trên PCB khác, ghi lại và báo lại")
print()

# Thử với các mapping có sẵn
mappings = ["regular", "classic", "adafruit-hat"]

for mapping in mappings:
    print(f"\nThử với mapping: {mapping}")
    try:
        opts = RGBMatrixOptions()
        opts.rows = 32
        opts.cols = 64
        opts.chain_length = 1
        opts.parallel = 1
        opts.hardware_mapping = mapping
        opts.gpio_slowdown = 4
        opts.brightness = 100
        opts.disable_hardware_pulsing = True
        opts.drop_privileges = False
        
        matrix = RGBMatrix(options=opts)
        canvas = matrix.CreateFrameCanvas()
        canvas.Fill(255, 255, 255)
        matrix.SwapOnVSync(canvas)
        print(f"  → Đã gửi màu trắng với mapping '{mapping}'")
        time.sleep(2)
        matrix.Clear()
    except Exception as e:
        print(f"  ✗ Lỗi: {e}")

print("\n" + "=" * 70)
print("QUAN TRỌNG:")
print("=" * 70)
print("Nếu không thấy đèn sáng, vui lòng:")
print("1. Kiểm tra sơ đồ chân IN TRÊN PCB của module LED")
print("2. So sánh với sơ đồ trong KET_NOI_HARDWARE.md")
print("3. Kiểm tra kết nối GPIO thực tế")
print("4. Đảm bảo nguồn 5V đã được cấp")
print("5. Đảm bảo cáp IDC đã cắm đúng chiều")
print()

