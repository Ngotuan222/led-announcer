#!/usr/bin/env python3
"""
Test đơn giản nhất - chỉ vẽ một điểm duy nhất
"""

import sys
from pathlib import Path
import yaml

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from rgbmatrix import RGBMatrix, RGBMatrixOptions
import time

print("="*50)
print("SINGLE POINT TEST")
print("="*50)

config_path = project_root / "config" / "settings.yaml"
with config_path.open("r", encoding="utf-8") as handle:
    config = yaml.safe_load(handle)

led_config = config.get("led", {})

rows = led_config.get("rows", 32)
cols = led_config.get("cols", 64)
chain_length = led_config.get("chain_length", 1)
parallel = led_config.get("parallel", 1)
brightness = led_config.get("brightness", 100)

options = RGBMatrixOptions()
options.rows = rows  
options.cols = cols  
options.chain_length = chain_length
options.parallel = 1  
options.brightness = 100  # Tăng brightness
options.drop_privileges = False
options.disable_hardware_pulsing = True  
options.scan_mode = 0  
options.hardware_mapping = "regular"  
options.multiplexing = 0  # Default multiplexing  
options.row_addr_type = 0  # Thử row address type
options.col_addr_type = 0  # Thử column address type  

try:
    matrix = RGBMatrix(options=options)
    print(f"✓ LED Matrix {rows}x{cols} khởi tạo thành công!")
    
    # Xóa toàn bộ matrix
    matrix.Clear()
    
    # Tạo canvas mới
    canvas = matrix.CreateFrameCanvas()
    canvas.Clear()
    
    # Vẽ một điểm duy nhất ở góc trên bên trái để kiểm tra
    center_x = 0   # Góc trên bên trái
    center_y = 0   # Góc trên bên trái
    
    print(f"Vẽ điểm duy nhất tại ({center_x}, {center_y})")
    canvas.SetPixel(center_x, center_y, 255, 0, 0)  # Màu đỏ
    
    # Hiển thị - thử cách khác
    canvas = matrix.SwapOnVSync(canvas)
    
    print("Bạn có thấy chỉ MỘT ĐIỂM ĐỎ duy nhất không?")
    time.sleep(10)
    
    # Xóa
    matrix.Clear()
    print("✓ Hoàn tất!")
    
except Exception as e:
    print(f"✗ Lỗi: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
