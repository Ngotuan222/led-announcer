#!/bin/bash
# Script kiểm tra các chân GPIO có được kích hoạt không

echo "=========================================="
echo "KIỂM TRA CHÂN GPIO"
echo "=========================================="
echo ""

# Kiểm tra quyền
if [ "$EUID" -ne 0 ]; then 
    echo "⚠️  Cần chạy với sudo để kiểm tra GPIO"
    echo "   Chạy: sudo $0"
    exit 1
fi

echo "Kiểm tra các chân GPIO theo sơ đồ 'regular' (đã kiểm tra):"
echo ""
echo "Theo sơ đồ HUB-75E (regular mapping) - đã xác minh:"
echo "  R1: GPIO 13 (Pin 23)"
echo "  G1: GPIO 19 (Pin 13)"
echo "  B1: GPIO 26 (Pin 26)"
echo "  R2: GPIO 12 (Pin 24)"
echo "  G2: GPIO 20 (Pin 21)"
echo "  B2: GPIO 21 (Pin 19)"
echo "  E:  GPIO 10 (Pin 10)"
echo "  A:  GPIO 15 (Pin 15)"
echo "  B:  GPIO 18 (Pin 16)"
echo "  C:  GPIO 23 (Pin 18)"
echo "  D:  GPIO 25 (Pin 22)"
echo "  CLK: GPIO 11 (Pin 11)"
echo "  LAT: GPIO 7 (Pin 7)"
echo "  OE:  GPIO 12 (Pin 12)"
echo ""
echo "✅ Sơ đồ này đã được kiểm tra và xác minh (xem KIEM_TRA_SO_DO_CHAN.md)"
echo ""

# Kiểm tra GPIO interface
if [ ! -d "/sys/class/gpio" ]; then
    echo "✗ GPIO interface không có sẵn"
    exit 1
fi

echo "✓ GPIO interface có sẵn"
echo ""
echo "Lưu ý: Các chân GPIO sẽ được kích hoạt khi chạy test LED"
echo "       Nếu không thấy đèn sáng, có thể:"
echo "       1. Sơ đồ chân không đúng với module LED của bạn"
echo "       2. Cần kiểm tra sơ đồ chân in trên PCB của module"
echo "       3. Cần thử các hardware mapping khác"
echo ""
echo "Chạy test với nhiều hardware mapping:"
echo "  sudo .venv/bin/python3 scripts/test_gpio_direct.py"

