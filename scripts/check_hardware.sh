#!/usr/bin/env bash
# Script kiểm tra phần cứng và kết nối

echo "=== Kiểm tra phần cứng LED Matrix ==="
echo ""

# Kiểm tra GPIO
echo "1. Kiểm tra GPIO..."
if [ -d "/sys/class/gpio" ]; then
    echo "   ✓ GPIO interface có sẵn"
else
    echo "   ✗ GPIO interface không tìm thấy"
fi

# Kiểm tra quyền truy cập GPIO
echo ""
echo "2. Kiểm tra quyền truy cập GPIO..."
if groups | grep -q gpio; then
    echo "   ✓ User trong group gpio"
else
    echo "   ✗ User chưa trong group gpio"
    echo "   → Chạy: sudo usermod -a -G gpio $USER"
    echo "   → Sau đó đăng xuất và đăng nhập lại"
fi

# Kiểm tra nguồn điện
echo ""
echo "3. Kiểm tra nguồn điện..."
echo "   → Đảm bảo module LED đã được cấp nguồn 5V"
echo "   → Kiểm tra đèn LED trên module có sáng không"
echo "   → Nguồn phải đủ công suất (2-4A cho module đơn)"

# Kiểm tra kết nối cáp
echo ""
echo "4. Kiểm tra kết nối cáp..."
echo "   → Cáp IDC 16-pin đã được cắm chắc chắn"
echo "   → Cắm đúng chiều (rãnh định hướng)"
echo "   → Kết nối từ GPIO Raspberry Pi đến cổng DATA_IN của module"

# Kiểm tra cấu hình
echo ""
echo "5. Kiểm tra cấu hình..."
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [ -f "$PROJECT_ROOT/config/settings.yaml" ]; then
    echo "   ✓ File cấu hình tồn tại"
    echo "   → Xem cấu hình: cat $PROJECT_ROOT/config/settings.yaml"
else
    echo "   ✗ File cấu hình không tìm thấy"
fi

echo ""
echo "=== Hướng dẫn kiểm tra ==="
echo ""
echo "1. Kiểm tra nguồn LED:"
echo "   - Module LED phải có đèn LED nguồn sáng"
echo "   - Nguồn 5V phải đủ công suất"
echo ""
echo "2. Kiểm tra cáp dữ liệu:"
echo "   - Cáp IDC 16-pin phải cắm chắc chắn"
echo "   - Cắm đúng chiều (không ngược)"
echo ""
echo "3. Kiểm tra GPIO:"
echo "   - Các chân GPIO phải kết nối đúng theo sơ đồ HUB-75E"
echo "   - Xem sơ đồ trong: KET_NOI_HARDWARE.md"
echo ""
echo "4. Test phần mềm:"
echo "   cd $PROJECT_ROOT"
echo "   ./scripts/test_led.sh"
echo ""

