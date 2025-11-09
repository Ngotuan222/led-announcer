# Kiểm Tra Sơ Đồ Chân GPIO

## ⚠️ VẤN ĐỀ: Không thấy đèn sáng với bất kỳ hardware mapping nào

Điều này cho thấy **sơ đồ chân GPIO có thể không đúng** với module LED của bạn.

## 🔍 BƯỚC 1: Kiểm Tra Sơ Đồ Chân Trên PCB

**Quan trọng nhất:** Xem sơ đồ chân **IN TRÊN PCB** của module LED của bạn.

1. Tìm sơ đồ chân ở gần cổng IDC 16-pin trên module LED
2. Sơ đồ thường in dạng:
   ```
   1: R1
   2: G1
   3: B1
   4: GND
   ...
   ```

## 📋 BƯỚC 2: So Sánh Với Sơ Đồ Hiện Tại

### Sơ đồ theo mapping "regular" (đã cập nhật):

| Chân IDC | Tín hiệu | GPIO | Pin vật lý |
|----------|----------|------|------------|
| 1        | R1       | 13   | 23         |
| 2        | G1       | 19   | 13         |
| 3        | B1       | 26   | 26         |
| 4        | GND      | GND  | -          |
| 5        | R2       | 12   | 24         |
| 6        | G2       | 20   | 21         |
| 7        | B2       | 21   | 19         |
| 8        | E        | 10   | 10         |
| 9        | A        | 15   | 15         |
| 10       | B        | 18   | 16         |
| 11       | C        | 23   | 18         |
| 12       | D        | 25   | 22         |
| 13       | CLK      | 11   | 11         |
| 14       | LAT      | 7    | 7          |
| 15       | OE       | 12   | 12         |
| 16       | GND      | GND  | -          |

### Sơ đồ ban đầu (có thể đúng với module của bạn):

| Chân IDC | Tín hiệu | GPIO | Pin vật lý |
|----------|----------|------|------------|
| 1        | R1       | 17   | 11         |
| 2        | G1       | 18   | 12         |
| 3        | B1       | 22   | 15         |
| 4        | GND      | GND  | -          |
| 5        | R2       | 23   | 16         |
| 6        | G2       | 24   | 18         |
| 7        | B2       | 25   | 22         |
| 8        | E        | 19   | 35         |
| 9        | A        | 26   | 37         |
| 10       | B        | 27   | 13         |
| 11       | C        | 5    | 29         |
| 12       | D        | 6    | 31         |
| 13       | CLK      | 21   | 40         |
| 14       | LAT      | 20   | 38         |
| 15       | OE       | 16   | 36         |
| 16       | GND      | GND  | -          |

## ✅ BƯỚC 3: Ghi Lại Sơ Đồ Chân Trên PCB

Nếu sơ đồ trên PCB **KHÁC** với cả hai sơ đồ trên, vui lòng ghi lại:

```
Chân IDC 1:  [tín hiệu] → GPIO [số] → Pin [số]
Chân IDC 2:  [tín hiệu] → GPIO [số] → Pin [số]
...
```

## 🔧 BƯỚC 4: Kiểm Tra Kết Nối GPIO Thực Tế

1. **Tắt nguồn Raspberry Pi**
2. **Kiểm tra từng kết nối:**
   - R1, G1, B1, R2, G2, B2 (màu)
   - A, B, C, D, E (địa chỉ)
   - CLK, LAT, OE (điều khiển)
   - GND (nối đất)
3. **Đảm bảo:**
   - Không có chân nào bị chạm nhau
   - Các chân GPIO đã kết nối đúng
   - Cáp IDC đã cắm chắc chắn và đúng chiều

## 🎯 BƯỚC 5: Test Lại

Sau khi kiểm tra, chạy lại test:

```bash
cd /home/loaled/Desktop/loaled/led_announcer
sudo .venv/bin/python3 scripts/test_gpio_direct.py
```

## 📝 THÔNG TIN CẦN CUNG CẤP

Nếu vẫn không hoạt động, cung cấp:

1. **Sơ đồ chân trên PCB của module LED** (ghi lại từng chân)
2. **Sơ đồ kết nối GPIO thực tế** (chân nào nối với GPIO nào)
3. **Module LED có đèn LED nguồn sáng không?**
4. **Cáp IDC đã cắm đúng chiều chưa?** (có rãnh định hướng)

## 💡 GIẢI PHÁP

Nếu sơ đồ chân trên PCB khác với các mapping có sẵn:

1. **Tạo custom hardware mapping** trong code
2. **Hoặc sử dụng adapter board/HAT** để tự động xử lý kết nối
3. **Hoặc điều chỉnh kết nối GPIO** theo sơ đồ trên PCB

