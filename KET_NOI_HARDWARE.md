# Hướng Dẫn Kết Nối Raspberry Pi 4 Model B với Màn Hình LED P4

## Tổng Quan

Dựa trên hình ảnh, bạn có:
- **Raspberry Pi 4 Model B** với chân GPIO 40-pin đang trống
- **Module LED P4** (256x128, loại 2121-A2) với:
  - Cổng **DATA_IN** (16-pin IDC) - đầu vào dữ liệu
  - Cổng **DATA_OUT** (16-pin IDC) - đầu ra để daisy-chain
  - Cổng nguồn **VCC/GND** (4 chân) - cần nguồn 5V riêng

## Phương Án Kết Nối

### Phương Án 1: Sử dụng Adafruit RGB Matrix HAT (Khuyến nghị)

Nếu bạn có **Adafruit RGB Matrix HAT** hoặc tương tự:

1. **Gắn HAT lên Raspberry Pi:**
   - Tắt nguồn Raspberry Pi
   - Cắm HAT vào các chân GPIO 40-pin
   - Đảm bảo HAT được cắm đúng chiều (chân 1 của HAT khớp với chân 1 của GPIO)

2. **Kết nối cáp dữ liệu:**
   - Sử dụng cáp IDC 16-pin (thường đi kèm với HAT)
   - Một đầu cắm vào cổng trên HAT
   - Đầu còn lại cắm vào cổng **DATA_IN** của module LED đầu tiên
   - **Lưu ý:** Đảm bảo cắm đúng chiều (thường có rãnh định hướng)

3. **Kết nối nguồn:**
   - Module LED P4 cần nguồn 5V riêng (không dùng nguồn từ Raspberry Pi)
   - Kết nối nguồn 5V vào cổng **VCC/GND** trên module
   - **Cực tính:** VCC (5V) và GND (nối đất) - cắm đúng cực tính!

### Phương Án 2: Kết nối trực tiếp qua GPIO (Không dùng HAT)

Nếu không có HAT, bạn có thể kết nối trực tiếp nhưng cần cẩn thận:

#### Sơ đồ chân GPIO cho HUB75 Interface:

Cổng IDC 16-pin trên module LED sử dụng chuẩn HUB75 với các chân:

**Sơ đồ cổng IDC 16-pin (nhìn từ phía cắm):**
```
     ┌─────────────────┐
     │ 1  3  5  7  9  11 13 15 │  ← Hàng trên
     │ 2  4  6  8  10 12 14 16 │  ← Hàng dưới
     └─────────────────┘
     ↑
  Rãnh định hướng (key)

Chi tiết các chân:
Hàng trên:  R1  B1  R2  B2   A   C  CLK  OE
Hàng dưới:  G1 GND  G2   E   B   D  LAT GND
```

**Sơ đồ chân HUB-75E (theo mapping "regular" của rpi-rgb-led-matrix):**

> **Lưu ý:** Sơ đồ này dựa trên [tài liệu chính thức](https://github.com/hzeller/rpi-rgb-led-matrix/blob/master/wiring.md) của thư viện rpi-rgb-led-matrix với `hardware_mapping: regular`. Nếu module LED của bạn có sơ đồ chân khác (in trên PCB), bạn có thể cần tạo custom hardware mapping.

| Chân IDC | Tín hiệu | GPIO Raspberry Pi | Chân vật lý | Mô tả |
|----------|----------|-------------------|-------------|-------|
| 1        | R1 (Red 1) | GPIO 13 | Pin 23 | Màu đỏ - nửa trên |
| 2        | G1 (Green 1) | GPIO 19 | Pin 13 | Màu xanh lá - nửa trên |
| 3        | B1 (Blue 1) | GPIO 26 | Pin 26 | Màu xanh dương - nửa trên |
| 4        | **GND** | GND | Pin 6, 9, 14, 20, 25, 30, 34, 39 | Nối đất |
| 5        | R2 (Red 2) | GPIO 12 | Pin 24 | Màu đỏ - nửa dưới |
| 6        | G2 (Green 2) | GPIO 20 | Pin 21 | Màu xanh lá - nửa dưới |
| 7        | B2 (Blue 2) | GPIO 21 | Pin 19 | Màu xanh dương - nửa dưới |
| 8        | **E (Address E)** | GPIO 10 | Pin 10 | Địa chỉ hàng bit 4 (cho 64+ hàng) |
| 9        | A (Address A) | GPIO 15 | Pin 15 | Địa chỉ hàng bit 0 |
| 10       | B (Address B) | GPIO 18 | Pin 16 | Địa chỉ hàng bit 1 |
| 11       | C (Address C) | GPIO 23 | Pin 18 | Địa chỉ hàng bit 2 |
| 12       | D (Address D) | GPIO 25 | Pin 22 | Địa chỉ hàng bit 3 |
| 13       | CLK (Clock) | GPIO 11 | Pin 11 | Xung đồng hồ dữ liệu |
| 14       | LAT (Latch/Strobe) | GPIO 7 | Pin 7 | Chốt dữ liệu |
| 15       | OE (Output Enable) | GPIO 12 | Pin 12 | Bật/tắt đầu ra |
| 16       | **GND** | GND | Pin 6, 9, 14, 20, 25, 30, 34, 39 | Nối đất |

> **✅ Đã kiểm tra:** Sơ đồ này đã được xác minh và cập nhật theo sơ đồ chân thực tế trên PCB module LED (xem KIEM_TRA_SO_DO_CHAN.md).

**Lưu ý quan trọng:**
- Sơ đồ này sử dụng **hardware mapping "regular"** (mặc định) của thư viện rpi-rgb-led-matrix
- Module này sử dụng **HUB-75E** với **5 chân địa chỉ (A, B, C, D, E)** cho 64+ hàng (2^5 = 32 hàng)
- Có **2 chân GND** ở vị trí chân 4 và chân 16
- Chân **E** nằm ở vị trí **chân 8**, giữa B2 và A
- Với màn hình 256x128, module sử dụng 5 chân địa chỉ để quét 32 hàng
- **Nếu sử dụng HAT (như Adafruit RGB Matrix HAT)**, bạn cần dùng `hardware_mapping: adafruit-hat` và HAT sẽ tự động xử lý kết nối
- **Nếu module LED của bạn có sơ đồ chân khác** (in trên PCB), bạn có thể cần:
  - Kiểm tra lại sơ đồ trên PCB của module
  - Tạo custom hardware mapping trong code
  - Hoặc sử dụng các mapping có sẵn khác: `adafruit-hat`, `adafruit-hat-pwm`, `regular-pi1`, `classic`, v.v.
- **Tham khảo:** [rpi-rgb-led-matrix wiring.md](https://github.com/hzeller/rpi-rgb-led-matrix/blob/master/wiring.md)

**⚠️ CẢNH BÁO:** 
- Kết nối trực tiếp có thể gây hỏng nếu sai
- Khuyến nghị sử dụng HAT hoặc adapter board
- Kiểm tra kỹ sơ đồ chân của module LED cụ thể của bạn

## Kết Nối Nguồn Điện

### Yêu Cầu Nguồn:
- **Điện áp:** 5V DC
- **Dòng điện:** 
  - Module đơn: 2-4A (tùy độ sáng)
  - Hai module: 4-8A
  - **Không dùng nguồn USB của Raspberry Pi!**

### Cách Kết Nối:
1. Sử dụng nguồn adapter 5V riêng, đủ công suất
2. Kết nối VCC (5V) vào chân VCC trên cổng nguồn module
3. Kết nối GND vào chân GND trên cổng nguồn module
4. **Kiểm tra cực tính kỹ trước khi cấp nguồn!**

## Kết Nối Daisy-Chain (Nếu có nhiều module)

Nếu bạn có module thứ hai (như trong hình):

1. Sử dụng cáp IDC 16-pin thứ hai
2. Một đầu cắm vào cổng **DATA_OUT** của module đầu tiên
3. Đầu còn lại cắm vào cổng **DATA_IN** của module thứ hai
4. Cấp nguồn cho module thứ hai (có thể dùng chung nguồn nếu đủ công suất)

## Kiểm Tra Sau Kết Nối

1. **Kiểm tra kỹ:**
   - Tất cả cáp được cắm chắc chắn
   - Cực tính nguồn đúng (VCC/GND)
   - Không có chân GPIO nào bị chạm nhau

2. **Bật nguồn:**
   - Bật nguồn cho module LED TRƯỚC
   - Sau đó bật Raspberry Pi

3. **Kiểm tra phần mềm:**
   ```bash
   cd /home/loaled/Desktop/loaled/led_announcer
   source .venv/bin/activate
   python3 -c "from rgbmatrix import RGBMatrix; print('LED Matrix library OK')"
   ```

## Cấu Hình Phần Mềm

Cấu hình hiện tại trong `config/settings.yaml`:

```yaml
led:
  rows: 128
  cols: 256
  chain_length: 1  # Số module nối tiếp
  parallel: 1    # Số panel song song
  hardware_mapping: adafruit-hat  # Nếu dùng HAT
```

### Kết nối trực tiếp (không dùng HAT):
Cấu hình hiện tại đã được thiết lập cho kết nối trực tiếp:
- `hardware_mapping: regular` - cho kết nối GPIO trực tiếp
- Sử dụng sơ đồ chân HUB-75E ở trên để kết nối

**Lưu ý quan trọng:**
- Khi kết nối trực tiếp, cần đảm bảo các chân GPIO được kết nối đúng theo sơ đồ
- Có thể cần điều chỉnh `gpio_slowdown` (thử 2, 3, 4, 5) nếu LED nhấp nháy
- Có thể cần chạy với quyền `sudo` để truy cập GPIO

## Xử Lý Sự Cố

### LED không sáng:
- Kiểm tra nguồn điện (đủ 5V, đủ dòng)
- Kiểm tra cáp dữ liệu (cắm đúng chiều)
- Kiểm tra cấu hình `hardware_mapping`

### LED nhấp nháy hoặc hiển thị sai:
- Điều chỉnh `gpio_slowdown` trong config (thử 2, 3, 4)
- Kiểm tra chất lượng cáp dữ liệu
- Kiểm tra nguồn điện có ổn định không

### Lỗi khi khởi động:
- Kiểm tra thư viện `rpi-rgb-led-matrix` đã cài đặt chưa
- Kiểm tra quyền truy cập GPIO (có thể cần sudo hoặc thêm user vào group gpio)

## Tài Liệu Tham Khảo

- [rpi-rgb-led-matrix GitHub](https://github.com/hzeller/rpi-rgb-led-matrix)
- [Adafruit RGB Matrix HAT](https://www.adafruit.com/product/2345)
- Sơ đồ chân GPIO Raspberry Pi 4: https://pinout.xyz

## Lưu Ý An Toàn

1. **Luôn tắt nguồn trước khi kết nối/ngắt kết nối**
2. **Kiểm tra cực tính nguồn kỹ trước khi cấp điện**
3. **Không cấp nguồn cho LED qua GPIO của Raspberry Pi**
4. **Sử dụng cáp chất lượng tốt, đủ tiết diện**
5. **Đảm bảo nguồn điện ổn định, không bị sụt áp**

