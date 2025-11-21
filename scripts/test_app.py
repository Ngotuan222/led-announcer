#!/usr/bin/env python3
"""
Test ứng dụng chính - hiển thị text trên LED
Chạy với: python3 scripts/test_app.py
Hoặc: sudo .venv/bin/python3 scripts/test_app.py
"""

import sys
import os
from pathlib import Path

project_root = Path(__file__).parent.parent
venv_python = project_root / ".venv" / "bin" / "python3"

# Nếu có venv nhưng hiện đang dùng Python hệ thống, chỉ cảnh báo (không thoát)
if not sys.executable.startswith(str(project_root)) and venv_python.exists():
    print("⚠️  Đang sử dụng Python hệ thống thay vì Python từ venv")
    print(f"   → Có thể chạy với: {venv_python} {sys.argv[0]}")


sys.path.insert(0, str(project_root))

from src.config import load_config
from src.display import LedDisplay
import time

print("="*70)
print("TEST ỨNG DỤNG CHÍNH - HIỂN THỊ TEXT TRÊN LED")
print("="*70)
print()

# Load config
config = load_config()
led_config = config.led

print(f"Cấu hình:")
print(f"  - Kích thước: {led_config.rows}x{led_config.cols}")
print(f"  - Chain length: {led_config.chain_length}")
print(f"  - Parallel: {led_config.parallel}")
print(f"  - Hardware mapping: {led_config.hardware_mapping}")
print(f"  - Brightness: {led_config.brightness}%")
print(f"  - Font: {led_config.font_path}")
print()

try:
    print("Đang khởi tạo LED Display...")
    display = LedDisplay(led_config)
    print("✓ LED Display khởi tạo thành công!\n")
    
    # Test 1: Hiển thị text đơn giản
    print("="*70)
    print("TEST 1: Hiển thị text 'TEST'")
    print("="*70)
    print("→ Bạn có thấy text 'TEST' hiển thị trên màn hình không?")
    print()
    display.show_text("TEST")
    print("✓ Đã hiển thị text 'TEST'\n")
    
    # Test 2: Hiển thị tên tiếng Việt
    print("="*70)
    print("TEST 2: Hiển thị tên tiếng Việt (chạy ngang)")
    print("="*70)
    print("→ Bạn có thấy text 'NGUYỄN VĂN A' chạy ngang không?")
    print()
    display.show_scrolling_text("NGUYỄN VĂN A", scroll_speed=0.15)
    print("✓ Đã hiển thị text 'NGUYỄN VĂN A'\n")
    
    # Test 3: Hiển thị text dài
    print("="*70)
    print("TEST 3: Hiển thị text dài (chạy ngang)")
    print("="*70)
    print("→ Bạn có thấy text 'LED MATRIX TEST' chạy ngang không?")
    print()
    display.show_scrolling_text("LED MATRIX TEST", scroll_speed=0.15)
    print("✓ Đã hiển thị text 'LED MATRIX TEST'\n")
    
    # Xóa màn hình
    print("Đang xóa màn hình...")
    display.clear()
    print("✓ Hoàn tất!\n")
    
    print("="*70)
    print("KẾT QUẢ: Tất cả test đều thành công!")
    print("="*70)
    print()
    print("Bước tiếp theo:")
    print("  1. Chạy dịch vụ chính:")
    print("     cd /home/loaled/Desktop/loaled/led_announcer")
    print("     source .venv/bin/activate")
    print("     uvicorn src.main:app --host 0.0.0.0 --port 8000")
    print()
    print("  2. Test API với curl:")
    print("     curl -X POST http://localhost:8000/announce \\")
    print("       -H 'Content-Type: application/json' \\")
    print("       -d '{\"id\":\"001\",\"fullname\":\"Nguyễn Văn A\"}'")
    print()
    
except Exception as e:
    print(f"\n✗ Lỗi: {e}")
    import traceback
    traceback.print_exc()
    print("\nKiểm tra:")
    print("  1. File font có tồn tại không?")
    print("  2. Cấu hình trong config/settings.yaml")
    print("  3. Quyền truy cập GPIO (có thể cần sudo)")
    sys.exit(1)

