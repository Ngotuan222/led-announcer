# Checklist Kiểm Tra Phần Cứng LED Matrix

## ⚠️ QUAN TRỌNG: Phần mềm đã chạy thành công nhưng màn hình không hiển thị

Điều này có nghĩa là vấn đề nằm ở **phần cứng hoặc kết nối**.

## ✅ Checklist Kiểm Tra

### 1. Nguồn Điện (QUAN TRỌNG NHẤT)

- [ ] **Module LED đã được cấp nguồn 5V riêng?**
  - Module LED cần nguồn 5V riêng, KHÔNG dùng nguồn từ Raspberry Pi
  - Nguồn phải đủ công suất: 2-4A cho module đơn, 4-8A cho 2 module
  
- [ ] **Đèn LED nguồn trên module có sáng không?**
  - Kiểm tra xem có đèn LED nhỏ nào trên module sáng không
  - Nếu không có đèn sáng → nguồn chưa được cấp hoặc sai cực tính

- [ ] **Kiểm tra cực tính nguồn:**
  - VCC (5V) → VCC trên module
  - GND → GND trên module
  - **CỰC TÍNH SAI SẼ HỎNG MODULE!**

### 2. Kết Nối Cáp Dữ Liệu

- [ ] **Cáp IDC 16-pin đã được cắm?**
  - Một đầu: GPIO Raspberry Pi (hoặc HAT nếu có)
  - Đầu kia: Cổng **DATA_IN** trên module LED

- [ ] **Cáp đã cắm chắc chắn?**
  - Kiểm tra xem cáp có bị lỏng không
  - Thử rút ra và cắm lại

- [ ] **Cáp đã cắm đúng chiều?**
  - Cáp IDC có rãnh định hướng (key)
  - Đảm bảo cắm đúng chiều, không ngược

### 3. Kết Nối GPIO (Nếu kết nối trực tiếp)

- [ ] **Đã kết nối đúng theo sơ đồ HUB-75E?**
  - Xem sơ đồ chi tiết trong `KET_NOI_HARDWARE.md`
  - Kiểm tra từng chân:
    - R1, G1, B1, R2, G2, B2 (màu)
    - A, B, C, D, E (địa chỉ)
    - CLK, LAT, OE (điều khiển)
    - GND (nối đất)

- [ ] **Không có chân nào bị chạm nhau?**
  - Kiểm tra xem các dây có bị chạm nhau không

### 4. Thứ Tự Bật Nguồn

- [ ] **Bật nguồn cho module LED TRƯỚC**
- [ ] **Sau đó mới bật Raspberry Pi**

**Thứ tự sai có thể gây lỗi!**

### 5. Kiểm Tra Module LED

- [ ] **Module LED có đèn LED nguồn sáng không?**
- [ ] **Module có bị hỏng không?**
  - Kiểm tra xem có mùi khét, vết cháy không
  - Kiểm tra các linh kiện trên board

## 🔧 Các Bước Khắc Phục

### Bước 1: Kiểm tra nguồn điện

```bash
# Kiểm tra nguồn 5V
# Sử dụng đồng hồ đo hoặc kiểm tra bằng đèn LED trên module
```

### Bước 2: Kiểm tra cáp dữ liệu

1. Rút cáp ra
2. Kiểm tra xem các chân có bị cong, gãy không
3. Cắm lại chắc chắn
4. Đảm bảo cắm đúng chiều

### Bước 3: Kiểm tra kết nối GPIO (nếu kết nối trực tiếp)

1. Tắt nguồn Raspberry Pi
2. Kiểm tra từng kết nối theo sơ đồ
3. Đảm bảo không có chân nào bị chạm nhau
4. Bật lại nguồn

### Bước 4: Test với cấu hình đơn giản

Thử với cấu hình đơn giản nhất:

```yaml
led:
  rows: 32
  cols: 64
  chain_length: 1
  parallel: 1
  hardware_mapping: regular
  disable_hardware_pulse: true
```

### Bước 5: Test với sudo (nếu cần)

```bash
cd /home/loaled/Desktop/loaled/led_announcer
sudo .venv/bin/python3 scripts/test_led_simple.py
```

## 🎯 Câu Hỏi Kiểm Tra

Trả lời các câu hỏi sau:

1. **Module LED có đèn LED nguồn sáng không?**
   - Có → Nguồn OK
   - Không → Kiểm tra nguồn điện

2. **Cáp IDC 16-pin đã được cắm chưa?**
   - Có → Kiểm tra cắm đúng chiều
   - Không → Cắm cáp

3. **Bạn đang kết nối trực tiếp hay dùng HAT?**
   - Trực tiếp → Kiểm tra sơ đồ GPIO
   - HAT → Kiểm tra HAT đã được gắn đúng chưa

4. **Bạn đã bật nguồn cho module LED trước khi bật Pi chưa?**
   - Có → OK
   - Không → Thử lại với thứ tự đúng

## 📞 Thông Tin Cần Cung Cấp

Nếu vẫn không hoạt động, cung cấp:

1. Module LED có đèn LED nguồn sáng không?
2. Cáp IDC đã được cắm chưa?
3. Bạn đang kết nối trực tiếp hay dùng HAT?
4. Có lỗi gì khi chạy test không?
5. Màn hình LED có phản ứng gì không (nhấp nháy, sáng nhẹ, v.v.)?

## ⚠️ Lưu Ý An Toàn

- **LUÔN tắt nguồn trước khi kết nối/ngắt kết nối**
- **Kiểm tra cực tính nguồn kỹ trước khi cấp điện**
- **Không cấp nguồn cho LED qua GPIO của Raspberry Pi**
- **Sử dụng nguồn ổn định, đủ công suất**

