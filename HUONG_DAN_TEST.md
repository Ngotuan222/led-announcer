# Hướng Dẫn Test Màn Hình LED Matrix

## ⚠️ Trước Khi Test - Kiểm Tra Phần Cứng

### 1. Kiểm tra kết nối phần cứng:
- ✅ **Cáp IDC 16-pin** đã kết nối giữa Raspberry Pi và module LED
- ✅ **Nguồn 5V** đã được cấp cho module LED (không dùng nguồn từ Pi)
- ✅ Tất cả kết nối đã chắc chắn, không bị lỏng
- ✅ Module LED đã được **bật nguồn TRƯỚC** khi bật Raspberry Pi
- ✅ Kiểm tra sơ đồ chân GPIO đã đúng (xem `KIEM_TRA_SO_DO_CHAN.md`)

### 2. Kiểm tra phần mềm:
- ✅ Đã cài đặt `rpi-rgb-led-matrix` và Python bindings
- ✅ Đã cài đặt các dependencies Python (xem `requirements.txt`)
- ✅ Virtual environment đã được kích hoạt

### 3. Kiểm tra cấu hình:
- ✅ File `config/settings.yaml` tồn tại
- ✅ `hardware_mapping: regular` (đã được kiểm tra và xác minh)
- ✅ Các thông số `rows`, `cols`, `chain_length`, `parallel` phù hợp với module LED của bạn

## 🚀 Các Cách Test Màn Hình

### Cách 1: Test Nhanh (Khuyến nghị cho lần đầu)

Script tự động kiểm tra và test cơ bản:

```bash
cd /home/loaled/Desktop/loaled/led_announcer
./scripts/test_led_connection.sh
```

**Script này sẽ:**
- ✅ Kiểm tra thư viện rgbmatrix đã cài đặt
- ✅ Kiểm tra quyền truy cập GPIO
- ✅ Kiểm tra file cấu hình
- ✅ Thử khởi tạo LED Matrix
- ✅ Test hiển thị frame đen

**Kết quả mong đợi:**
- Tất cả bước đều hiển thị ✓
- Không có lỗi
- Màn hình LED có thể tắt (hiển thị đen)

---

### Cách 2: Test Đơn Giản với Màu Sắc

Test hiển thị các màu cơ bản và text:

```bash
cd /home/loaled/Desktop/loaled/led_announcer
./scripts/test_led.sh
```

Hoặc chạy trực tiếp:

```bash
cd /home/loaled/Desktop/loaled/led_announcer
source .venv/bin/activate
python3 scripts/test_led_simple.py
```

**Nếu cần quyền root:**
```bash
sudo .venv/bin/python3 scripts/test_led_simple.py
```

**Script này sẽ:**
- ✅ Hiển thị màn hình đen (2 giây)
- ✅ Hiển thị màu đỏ (2 giây)
- ✅ Hiển thị màu xanh lá (2 giây)
- ✅ Hiển thị màu xanh dương (2 giây)
- ✅ Hiển thị text "TEST" (3 giây)

**Kết quả mong đợi:**
- Bạn thấy màn hình sáng với các màu tương ứng
- Text "TEST" hiển thị rõ ràng

---

### Cách 3: Test Tối Thiểu (Nếu các test trên không hoạt động)

Test với cấu hình đơn giản nhất (32x64, 1 panel):

```bash
cd /home/loaled/Desktop/loaled/led_announcer
source .venv/bin/activate
sudo .venv/bin/python3 scripts/test_minimal.py
```

**Script này sẽ:**
- ✅ Test với cấu hình tối thiểu: 32x64, chain=1, parallel=1
- ✅ Hiển thị màu trắng (5 giây) - sáng nhất
- ✅ Hiển thị màu đỏ (3 giây)
- ✅ Hiển thị màu xanh lá (3 giây)
- ✅ Hiển thị màu xanh dương (3 giây)

**Khi nào dùng:**
- Nếu test với cấu hình đầy đủ không hoạt động
- Để xác nhận kết nối cơ bản có hoạt động không
- Nếu test này OK, thử tăng `chain_length` và `parallel` trong config

---

### Cách 4: Test Nhiều Hardware Mapping (Nếu không thấy đèn sáng)

Thử tất cả các hardware mapping có sẵn để tìm mapping phù hợp:

```bash
cd /home/loaled/Desktop/loaled/led_announcer
source .venv/bin/activate
sudo .venv/bin/python3 scripts/test_gpio_direct.py
```

**Script này sẽ:**
- ✅ Thử lần lượt các mapping: `regular`, `regular-pi1`, `classic`, `classic-pi1`, `adafruit-hat`, `adafruit-hat-pwm`
- ✅ Với mỗi mapping, hiển thị màu trắng, đỏ, xanh lá
- ✅ Hỏi bạn có thấy đèn sáng không

**Khi nào dùng:**
- Nếu không thấy đèn sáng với mapping `regular`
- Nếu sơ đồ chân trên PCB module LED khác với sơ đồ đã kiểm tra
- Để tìm hardware mapping phù hợp với module LED của bạn

**Lưu ý:** 
- Script sẽ dừng khi bạn nhập `y` (yes) cho mapping nào đó
- Sau đó cập nhật `hardware_mapping` trong `config/settings.yaml`

---

### Cách 5: Test với Dịch Vụ Chính

Test thông qua API của ứng dụng:

```bash
cd /home/loaled/Desktop/loaled/led_announcer
source .venv/bin/activate
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

Sau đó test bằng curl:

```bash
curl -X POST http://localhost:8000/announce \
  -H "Content-Type: application/json" \
  -d '{"id":"test","fullname":"Test LED"}'
```

**Kết quả mong đợi:**
- Dịch vụ khởi động thành công
- Text "Test LED" hiển thị trên màn hình LED
- API trả về status 200

---

## 🔍 Kiểm Tra Sơ Đồ Chân GPIO

Nếu không thấy đèn sáng, kiểm tra sơ đồ chân:

```bash
cd /home/loaled/Desktop/loaled/led_announcer
python3 scripts/check_pinout.py
```

Script này sẽ hiển thị:
- Sơ đồ chân IDC 16-pin
- Mapping GPIO theo `regular` (đã được kiểm tra)
- Hướng dẫn so sánh với sơ đồ trên PCB module LED

**Xem chi tiết:** `KIEM_TRA_SO_DO_CHAN.md`

---

## ⚙️ Cấu Hình Test

### Cấu hình cho HUB-75E (256x128) - 1 module:

```yaml
led:
  rows: 128
  cols: 256
  chain_length: 1      # Số module nối tiếp
  parallel: 1          # Số panel song song
  hardware_mapping: regular  # ✅ Đã được kiểm tra và xác minh
  gpio_slowdown: 4     # Thử 2-6 nếu có vấn đề
  brightness: 70       # 0-100
```

### Cấu hình cho nhiều module nối tiếp:

```yaml
led:
  rows: 32
  cols: 64
  chain_length: 4      # 4 module nối tiếp
  parallel: 2          # 2 panel song song
  hardware_mapping: regular
  gpio_slowdown: 4
  brightness: 70
```

**Lưu ý:**
- `chain_length`: Số module nối tiếp (tăng chiều ngang)
- `parallel`: Số panel song song (tăng chiều dọc)
- Tổng kích thước = `cols * chain_length` x `rows * parallel`

---

## 🐛 Xử Lý Lỗi Thường Gặp

### Lỗi: "rgbmatrix bindings could not be imported"

**Nguyên nhân:** Chưa cài đặt thư viện rpi-rgb-led-matrix

**Giải pháp:**
```bash
# Clone repository
cd ~
git clone https://github.com/hzeller/rpi-rgb-led-matrix.git
cd rpi-rgb-led-matrix

# Build và cài đặt
make build-python
sudo make install-python

# Hoặc cài đặt Python bindings
cd bindings/python
sudo python3 setup.py install
```

---

### Lỗi: "Permission denied" hoặc "GPIO access denied"

**Nguyên nhân:** Không có quyền truy cập GPIO

**Giải pháp 1:** Thêm user vào group gpio (khuyến nghị)
```bash
sudo usermod -a -G gpio $USER
# Đăng xuất và đăng nhập lại
```

**Giải pháp 2:** Chạy với sudo
```bash
sudo .venv/bin/python3 scripts/test_led_simple.py
```

---

### Lỗi: "LED display unavailable" hoặc "Failed to initialize"

**Nguyên nhân:** 
- Kết nối phần cứng chưa đúng
- Nguồn điện chưa được cấp
- Cấu hình hardware_mapping sai

**Giải pháp:**
1. ✅ Kiểm tra lại cáp IDC 16-pin (cắm đúng chiều, chắc chắn)
2. ✅ Kiểm tra nguồn 5V cho LED (đủ công suất, đã bật)
3. ✅ Kiểm tra cấu hình trong `config/settings.yaml`:
   - `hardware_mapping: regular` (đã được kiểm tra)
   - `gpio_slowdown`: Thử các giá trị 2, 3, 4, 5, 6
4. ✅ Kiểm tra sơ đồ chân GPIO (xem `KIEM_TRA_SO_DO_CHAN.md`)
5. ✅ Thử test với nhiều hardware mapping (Cách 4)

---

### Lỗi: LED nhấp nháy hoặc hiển thị sai

**Nguyên nhân:**
- GPIO slowdown chưa phù hợp
- Nguồn điện không ổn định
- Cáp dữ liệu chất lượng kém

**Giải pháp:**
1. Tăng `gpio_slowdown` trong config (thử 5, 6, 7)
2. Kiểm tra nguồn điện (đủ 5V, đủ dòng, ổn định)
3. Thử cáp khác hoặc kiểm tra tiếp xúc
4. Kiểm tra cáp không quá dài (khuyến nghị < 1m)

---

### Lỗi: "Font file not found"

**Nguyên nhân:** Đường dẫn font không đúng

**Giải pháp:**
1. Kiểm tra font có tồn tại:
   ```bash
   ls -la /home/pi/rpi-rgb-led-matrix/fonts/
   ```

2. Cập nhật đường dẫn trong `config/settings.yaml`:
   ```yaml
   led:
     font_path: /đường/dẫn/đến/font.bdf
   ```

3. Hoặc tải font từ repository:
   ```bash
   cd ~/rpi-rgb-led-matrix/fonts
   # Các font có sẵn: 4x6.bdf, 5x7.bdf, 6x9.bdf, 6x10.bdf, 6x12.bdf, 6x13.bdf, 6x13B.bdf, 6x13O.bdf, 7x13.bdf, 7x13B.bdf, 7x13O.bdf, 7x14.bdf, 7x14B.bdf, 8x13.bdf, 8x13B.bdf, 8x13O.bdf, 9x15.bdf, 9x15B.bdf, 9x18.bdf, 9x18B.bdf, 10x20.bdf, 12x22.bdf, 18x34.bdf
   ```

---

## ✅ Test Thành Công

Nếu tất cả test đều OK, bạn sẽ thấy:
- ✅ LED Matrix khởi tạo thành công
- ✅ Màn hình hiển thị các màu đúng
- ✅ Text hiển thị rõ ràng
- ✅ Không có lỗi trong log

---

## 📋 Checklist Test

Trước khi test, đảm bảo:

- [ ] Nguồn 5V đã được cấp cho module LED
- [ ] Cáp IDC 16-pin đã cắm chắc chắn
- [ ] Module LED đã bật nguồn TRƯỚC khi bật Raspberry Pi
- [ ] Sơ đồ chân GPIO đã đúng (xem `KIEM_TRA_SO_DO_CHAN.md`)
- [ ] File `config/settings.yaml` có `hardware_mapping: regular`
- [ ] Thư viện rgbmatrix đã được cài đặt
- [ ] User đã trong group gpio hoặc có quyền sudo

---

## 🎯 Bước Tiếp Theo

Sau khi test thành công:

1. **Chạy dịch vụ chính:**
   ```bash
   cd /home/loaled/Desktop/loaled/led_announcer
   source .venv/bin/activate
   uvicorn src.main:app --host 0.0.0.0 --port 8000
   ```

2. **Test API với Postman hoặc curl:**
   ```bash
   curl -X POST http://localhost:8000/announce \
     -H "Content-Type: application/json" \
     -d '{"id":"001","fullname":"Nguyễn Văn A"}'
   ```

3. **Cấu hình systemd service** (tùy chọn) để tự động khởi động

4. **Điều chỉnh brightness, font, màu sắc** theo nhu cầu trong `config/settings.yaml`

---

## ⚠️ Lưu Ý An Toàn

- ⚠️ **Luôn tắt nguồn** trước khi kết nối/ngắt kết nối
- ⚠️ **Kiểm tra cực tính nguồn** kỹ trước khi cấp điện
- ⚠️ **Không cấp nguồn cho LED** qua GPIO của Raspberry Pi
- ⚠️ **Sử dụng nguồn ổn định**, đủ công suất (2-4A cho 1 module)
- ⚠️ **Kiểm tra cáp IDC** không bị chạm chập

---

## 📚 Tài Liệu Tham Khảo

- `KIEM_TRA_SO_DO_CHAN.md` - Kiểm tra sơ đồ chân GPIO
- `KET_NOI_HARDWARE.md` - Hướng dẫn kết nối phần cứng
- `KIEM_TRA_PHAN_CUNG.md` - Checklist kiểm tra phần cứng
- [rpi-rgb-led-matrix Documentation](https://github.com/hzeller/rpi-rgb-led-matrix)
