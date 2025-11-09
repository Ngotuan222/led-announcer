#!/usr/bin/env python3
"""
Test LED với màu sáng rõ ràng - để kiểm tra xem LED có sáng không
Chạy với: sudo .venv/bin/python3 scripts/test_led_bright.py
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

print("\n" + "="*70)
print("TEST LED VỚI MÀU SÁNG - KIỂM TRA XEM LED CÓ SÁNG KHÔNG")
print("="*70)
print()

# Đọc cấu hình
config_path = project_root / "config" / "settings.yaml"
if not config_path.exists():
    print(f"✗ Không tìm thấy file cấu hình: {config_path}")
    sys.exit(1)

import yaml
with open(config_path) as f:
    config = yaml.safe_load(f)

led_config = config.get("led", {})

# Tạo options
options = RGBMatrixOptions()
options.rows = led_config.get("rows", 32)
options.cols = led_config.get("cols", 64)
options.chain_length = led_config.get("chain_length", 1)
options.parallel = led_config.get("parallel", 1)
options.hardware_mapping = led_config.get("hardware_mapping", "regular")
options.gpio_slowdown = led_config.get("gpio_slowdown", 4)
options.brightness = 100  # Độ sáng tối đa để dễ thấy
options.drop_privileges = False
if led_config.get("disable_hardware_pulse", True):
    options.disable_hardware_pulsing = True

print(f"Cấu hình:")
print(f"  - Kích thước: {options.rows}x{options.cols}")
print(f"  - Chain length: {options.chain_length}")
print(f"  - Parallel: {options.parallel}")
print(f"  - Hardware mapping: {options.hardware_mapping}")
print(f"  - Brightness: {options.brightness}% (tối đa)")
print()

try:
    print("Đang khởi tạo LED Matrix...")
    matrix = RGBMatrix(options=options)
    print("✓ LED Matrix khởi tạo thành công!\n")
    
    import time
    
    print("="*70)
    print("BẮT ĐẦU TEST - QUAN SÁT MÀN HÌNH LED")
    print("="*70)
    print()
    
    # Test 1: Màu trắng (sáng nhất)
    print(">>> TEST 1: MÀU TRẮNG (sáng nhất) - 10 giây <<<")
    print("   → Bạn có thấy màn hình sáng TRẮNG không?")
    print()
    canvas = matrix.CreateFrameCanvas()
    canvas.Fill(255, 255, 255)  # Trắng
    matrix.SwapOnVSync(canvas)
    time.sleep(10)
    print("   ✓ Đã hiển thị màu trắng 10 giây\n")
    
    # Test 2: Màu đỏ
    print(">>> TEST 2: MÀU ĐỎ - 5 giây <<<")
    print("   → Bạn có thấy màn hình sáng ĐỎ không?")
    print()
    canvas.Fill(255, 0, 0)  # Đỏ
    matrix.SwapOnVSync(canvas)
    time.sleep(5)
    print("   ✓ Đã hiển thị màu đỏ 5 giây\n")
    
    # Test 3: Màu xanh lá
    print(">>> TEST 3: MÀU XANH LÁ - 5 giây <<<")
    print("   → Bạn có thấy màn hình sáng XANH LÁ không?")
    print()
    canvas.Fill(0, 255, 0)  # Xanh lá
    matrix.SwapOnVSync(canvas)
    time.sleep(5)
    print("   ✓ Đã hiển thị màu xanh lá 5 giây\n")
    
    # Test 4: Màu xanh dương
    print(">>> TEST 4: MÀU XANH DƯƠNG - 5 giây <<<")
    print("   → Bạn có thấy màn hình sáng XANH DƯƠNG không?")
    print()
    canvas.Fill(0, 0, 255)  # Xanh dương
    matrix.SwapOnVSync(canvas)
    time.sleep(5)
    print("   ✓ Đã hiển thị màu xanh dương 5 giây\n")
    
    # Test 5: Màu vàng (đỏ + xanh lá)
    print(">>> TEST 5: MÀU VÀNG - 5 giây <<<")
    print("   → Bạn có thấy màn hình sáng VÀNG không?")
    print()
    canvas.Fill(255, 255, 0)  # Vàng
    matrix.SwapOnVSync(canvas)
    time.sleep(5)
    print("   ✓ Đã hiển thị màu vàng 5 giây\n")
    
    # Xóa
    print("Đang xóa màn hình...")
    matrix.Clear()
    print("✓ Hoàn tất!\n")
    
    print("="*70)
    print("KẾT QUẢ")
    print("="*70)
    print()
    print("Nếu bạn KHÔNG thấy màn hình sáng với bất kỳ màu nào:")
    print()
    print("1. KIỂM TRA NGUỒN ĐIỆN:")
    print("   - Module LED có đèn LED nguồn sáng không?")
    print("   - Nguồn 5V đã được cấp chưa? (đủ 2-4A)")
    print("   - Cực tính đúng chưa? (VCC → VCC, GND → GND)")
    print()
    print("2. KIỂM TRA CÁP DỮ LIỆU:")
    print("   - Cáp IDC 16-pin đã cắm chưa?")
    print("   - Cắm vào cổng DATA_IN trên module chưa?")
    print("   - Cáp đã cắm chắc chắn chưa?")
    print("   - Cáp đã cắm đúng chiều chưa? (rãnh định hướng)")
    print()
    print("3. KIỂM TRA GPIO:")
    print("   - Các chân GPIO đã kết nối đúng theo sơ đồ chưa?")
    print("   - Xem sơ đồ trong: KIEM_TRA_SO_DO_CHAN.md")
    print("   - Thử test với nhiều hardware mapping:")
    print("     sudo .venv/bin/python3 scripts/test_gpio_direct.py")
    print()
    print("4. KIỂM TRA CẤU HÌNH:")
    print("   - rows, cols, chain_length, parallel có đúng không?")
    print("   - Xem file: config/settings.yaml")
    print()
    print("5. THỨ TỰ BẬT NGUỒN:")
    print("   - Bật nguồn module LED TRƯỚC")
    print("   - Sau đó mới bật Raspberry Pi")
    print()
    print("Xem chi tiết: KIEM_TRA_PHAN_CUNG.md")
    print()
    
except Exception as e:
    print(f"\n✗ Lỗi: {e}")
    import traceback
    traceback.print_exc()
    print("\nKiểm tra:")
    print("  1. Kết nối phần cứng (cáp IDC 16-pin)")
    print("  2. Nguồn điện 5V cho LED")
    print("  3. Cấu hình hardware_mapping")
    print("  4. Quyền truy cập GPIO (có thể cần sudo)")
    sys.exit(1)

