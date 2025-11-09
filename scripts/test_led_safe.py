#!/usr/bin/env python3
"""
Script test an toàn - chỉ kiểm tra import và cấu hình, không khởi tạo hardware
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

print("=== Kiểm tra cấu hình LED Matrix ===\n")

# Kiểm tra import
try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions
    print("✓ Thư viện rgbmatrix OK")
except ImportError as e:
    print(f"✗ Không thể import rgbmatrix: {e}")
    print("→ Cần cài đặt rpi-rgb-led-matrix")
    sys.exit(1)

# Đọc cấu hình
config_path = project_root / "config" / "settings.yaml"
if not config_path.exists():
    print(f"✗ Không tìm thấy file cấu hình: {config_path}")
    sys.exit(1)

import yaml
with open(config_path) as f:
    config = yaml.safe_load(f)

led_config = config.get("led", {})

# Tạo options (không khởi tạo matrix)
options = RGBMatrixOptions()
options.rows = led_config.get("rows", 32)
options.cols = led_config.get("cols", 64)
options.chain_length = led_config.get("chain_length", 1)
options.parallel = led_config.get("parallel", 1)
options.hardware_mapping = led_config.get("hardware_mapping", "regular")
options.gpio_slowdown = led_config.get("gpio_slowdown", 4)
options.brightness = led_config.get("brightness", 70)

print(f"\nCấu hình:")
print(f"  - Kích thước panel: {options.rows}x{options.cols}")
print(f"  - Chain length: {options.chain_length}")
print(f"  - Parallel: {options.parallel}")
print(f"  - Hardware mapping: {options.hardware_mapping}")
print(f"  - GPIO slowdown: {options.gpio_slowdown}")
print(f"  - Brightness: {options.brightness}%")

total_cols = options.cols * options.chain_length
total_rows = options.rows * options.parallel
print(f"\nTổng kích thước: {total_cols}x{total_rows}")

# Kiểm tra giới hạn
if options.parallel < 1 or options.parallel > 3:
    print(f"\n⚠️  Cảnh báo: parallel={options.parallel} ngoài phạm vi cho phép (1-3)")
    print("   → Sửa trong config/settings.yaml")

if options.rows < 8 or options.rows > 64:
    print(f"\n⚠️  Cảnh báo: rows={options.rows} ngoài phạm vi cho phép (8-64)")

print("\n✓ Cấu hình hợp lệ (chưa test hardware)")
print("\nĐể test hardware, chạy:")
print("  python3 scripts/test_led_simple.py")
print("  (hoặc với sudo nếu cần quyền GPIO)")

