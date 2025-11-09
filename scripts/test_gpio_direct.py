#!/usr/bin/env python3
"""
Test GPIO trực tiếp - kiểm tra từng chân và thử nhiều hardware mapping
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from rgbmatrix import RGBMatrix, RGBMatrixOptions
import time

print("=" * 70)
print("TEST GPIO TRỰC TIẾP - KIỂM TRA TỪNG HARDWARE MAPPING")
print("=" * 70)

# Danh sách các hardware mapping để thử
mappings_to_try = [
    "regular",
    "regular-pi1",
    "classic",
    "classic-pi1",
    "adafruit-hat",
    "adafruit-hat-pwm",
]

# Cấu hình đơn giản nhất
base_config = {
    "rows": 32,
    "cols": 64,
    "chain_length": 1,
    "parallel": 1,
    "brightness": 100,
    "gpio_slowdown": 4,
}

print(f"\nCấu hình test: {base_config}")
print(f"Sẽ thử {len(mappings_to_try)} hardware mapping khác nhau\n")

for mapping in mappings_to_try:
    print(f"{'='*70}")
    print(f"THỬ HARDWARE MAPPING: {mapping}")
    print(f"{'='*70}")
    
    try:
        options = RGBMatrixOptions()
        options.rows = base_config["rows"]
        options.cols = base_config["cols"]
        options.chain_length = base_config["chain_length"]
        options.parallel = base_config["parallel"]
        options.hardware_mapping = mapping
        options.gpio_slowdown = base_config["gpio_slowdown"]
        options.brightness = base_config["brightness"]
        options.disable_hardware_pulsing = True
        options.drop_privileges = False
        
        print(f"Đang khởi tạo với mapping '{mapping}'...")
        matrix = RGBMatrix(options=options)
        print(f"✓ Khởi tạo thành công!")
        
        # Test 1: Màu trắng
        print(f"  → Gửi MÀU TRẮNG (3 giây)...")
        canvas = matrix.CreateFrameCanvas()
        canvas.Fill(255, 255, 255)
        matrix.SwapOnVSync(canvas)
        time.sleep(3)
        
        # Test 2: Màu đỏ
        print(f"  → Gửi MÀU ĐỎ (2 giây)...")
        canvas.Fill(255, 0, 0)
        matrix.SwapOnVSync(canvas)
        time.sleep(2)
        
        # Test 3: Màu xanh lá
        print(f"  → Gửi MÀU XANH LÁ (2 giây)...")
        canvas.Fill(0, 255, 0)
        matrix.SwapOnVSync(canvas)
        time.sleep(2)
        
        matrix.Clear()
        print(f"\n✓ Mapping '{mapping}' hoạt động!")
        print(f"\n>>> BẠN CÓ THẤY ĐÈN SÁNG VỚI MAPPING '{mapping}' KHÔNG? <<<")
        response = input("   (y/n, hoặc Enter để tiếp tục): ")
        
        if response.lower() == 'y':
            print(f"\n{'='*70}")
            print(f"THÀNH CÔNG! Hardware mapping đúng là: {mapping}")
            print(f"{'='*70}")
            print(f"\nCập nhật config/settings.yaml:")
            print(f"  hardware_mapping: {mapping}")
            sys.exit(0)
        
    except Exception as e:
        print(f"✗ Lỗi với mapping '{mapping}': {e}")
        continue

print(f"\n{'='*70}")
print("KHÔNG TÌM THẤY HARDWARE MAPPING PHÙ HỢP")
print(f"{'='*70}")
print("\nCó thể vấn đề là:")
print("  1. Sơ đồ chân GPIO không đúng với module LED của bạn")
print("  2. Module LED có sơ đồ chân khác (in trên PCB)")
print("  3. Cần kiểm tra lại kết nối GPIO thực tế")
print("\nKiểm tra:")
print("  - Xem sơ đồ chân in trên PCB của module LED")
print("  - So sánh với sơ đồ trong KET_NOI_HARDWARE.md")
print("  - Có thể cần tạo custom hardware mapping")

