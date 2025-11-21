#!/usr/bin/env python3
"""
Test đơn giản - chỉ vẽ một điểm để xác định tọa độ chính xác
Chạy với: sudo .venv/bin/python3 scripts/simple_center_test.py
"""

import sys
from pathlib import Path
import yaml

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from rgbmatrix import RGBMatrix, RGBMatrixOptions
import time

print("="*50)
print("SIMPLE CENTER TEST")
print("="*50)

config_path = project_root / "config" / "settings.yaml"
with config_path.open("r", encoding="utf-8") as handle:
    config = yaml.safe_load(handle)

led_config = config.get("led", {})

rows = led_config.get("rows", 40)
cols = led_config.get("cols", 80)
chain_length = led_config.get("chain_length", 1)
parallel = led_config.get("parallel", 1)
brightness = led_config.get("brightness", 100)

options = RGBMatrixOptions()
options.rows = rows
options.cols = cols
options.chain_length = chain_length
options.parallel = parallel
options.brightness = brightness
options.drop_privileges = False

try:
    matrix = RGBMatrix(options=options)
    print(f"✓ LED Matrix {rows}x{cols} khởi tạo thành công!")
    
    canvas = matrix.CreateFrameCanvas()
    
    # Thử các tọa độ khác nhau
    test_points = [
        (10, 10), (15, 15), (20, 10), (20, 20), (30, 15), (40, 20)
    ]
    
    for i, (x, y) in enumerate(test_points):
        print(f"\nTest {i+1}: Vẽ điểm tại ({x}, {y})")
        canvas.Clear()
        canvas.SetPixel(x, y, 0, 255, 0)  # Chỉ một điểm xanh
        matrix.SwapOnVSync(canvas)
        print(f"  → Bạn có thấy điểm XANH duy nhất tại ({x}, {y}) không?")
        time.sleep(3)
    
    canvas.Clear()
    print("\n✓ Hoàn tất!")
    
except Exception as e:
    print(f"✗ Lỗi: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
