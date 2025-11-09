#!/usr/bin/env python3
"""
Test tối thiểu - cấu hình đơn giản nhất để kiểm tra kết nối
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions
    print("✓ Thư viện rgbmatrix OK")
except ImportError as e:
    print(f"✗ Không thể import rgbmatrix: {e}")
    sys.exit(1)

print("\n=== Test với cấu hình tối thiểu ===")
print("Cấu hình: 32x64, chain=1, parallel=1")
print("(Nếu test này OK, thử tăng chain_length và parallel)\n")

# Cấu hình tối thiểu
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1  # Chỉ 1 panel
options.parallel = 1      # Chỉ 1 panel song song
options.hardware_mapping = "regular"
options.gpio_slowdown = 4
options.brightness = 100  # Độ sáng tối đa
options.disable_hardware_pulsing = True
options.drop_privileges = False

print("Đang khởi tạo LED Matrix...")
try:
    matrix = RGBMatrix(options=options)
    print("✓ Khởi tạo thành công!\n")
    
    import time
    
    # Test 1: Màu trắng (sáng nhất)
    print("Test 1: Màu TRẮNG (sáng nhất) - 5 giây...")
    canvas = matrix.CreateFrameCanvas()
    canvas.Fill(255, 255, 255)
    matrix.SwapOnVSync(canvas)
    time.sleep(5)
    print("  → Bạn có thấy màn hình sáng trắng không?\n")
    
    # Test 2: Màu đỏ
    print("Test 2: Màu ĐỎ - 3 giây...")
    canvas.Fill(255, 0, 0)
    matrix.SwapOnVSync(canvas)
    time.sleep(3)
    print("  → Bạn có thấy màn hình đỏ không?\n")
    
    # Test 3: Màu xanh lá
    print("Test 3: Màu XANH LÁ - 3 giây...")
    canvas.Fill(0, 255, 0)
    matrix.SwapOnVSync(canvas)
    time.sleep(3)
    print("  → Bạn có thấy màn hình xanh lá không?\n")
    
    # Test 4: Màu xanh dương
    print("Test 4: Màu XANH DƯƠNG - 3 giây...")
    canvas.Fill(0, 0, 255)
    matrix.SwapOnVSync(canvas)
    time.sleep(3)
    print("  → Bạn có thấy màn hình xanh dương không?\n")
    
    # Xóa
    print("Xóa màn hình...")
    matrix.Clear()
    print("✓ Hoàn tất!\n")
    
    print("=== Kết quả ===")
    print("Nếu bạn KHÔNG thấy màn hình sáng:")
    print("  1. Kiểm tra nguồn 5V cho module LED")
    print("  2. Kiểm tra cáp IDC 16-pin đã cắm chưa")
    print("  3. Kiểm tra kết nối GPIO (nếu kết nối trực tiếp)")
    print("  4. Xem checklist trong: KIEM_TRA_PHAN_CUNG.md")
    
except Exception as e:
    print(f"\n✗ Lỗi: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

