# Hướng Dẫn Sử Dụng LED Announcer

## ✅ LED Đã Sáng - Sẵn Sàng Sử Dụng!

Nếu LED đã sáng, bạn có thể bắt đầu sử dụng ứng dụng.

## 🚀 Các Bước Tiếp Theo

### Bước 1: Test Hiển Thị Text

Test hiển thị text trên LED:

```bash
cd /home/loaled/Desktop/loaled/led_announcer
source .venv/bin/activate
python3 scripts/test_app.py
```

Hoặc nếu cần quyền root:

```bash
sudo .venv/bin/python3 scripts/test_app.py
```

**Script này sẽ:**
- Hiển thị text "TEST"
- Hiển thị text "NGUYỄN VĂN A"
- Hiển thị text "LED MATRIX TEST"

---

### Bước 2: Chạy Dịch Vụ Chính

Khởi động dịch vụ API:

```bash
cd /home/loaled/Desktop/loaled/led_announcer
source .venv/bin/activate
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

**Dịch vụ sẽ chạy tại:**
- URL: `http://localhost:8000`
- API docs: `http://localhost:8000/docs` (Swagger UI)
- Health check: `http://localhost:8000/healthz`

---

### Bước 3: Test API

#### Test với curl:

```bash
# Test health check
curl http://localhost:8000/healthz

# Test announce
curl -X POST http://localhost:8000/announce \
  -H "Content-Type: application/json" \
  -d '{"id":"001","fullname":"Nguyễn Văn A"}'
```

#### Test với Python:

```python
import requests

# Test health check
response = requests.get("http://localhost:8000/healthz")
print(response.json())

# Test announce
response = requests.post(
    "http://localhost:8000/announce",
    json={"id": "001", "fullname": "Nguyễn Văn A"}
)
print(response.json())
```

#### Test với Postman hoặc trình duyệt:

1. Mở `http://localhost:8000/docs` trong trình duyệt
2. Chọn endpoint `/announce`
3. Click "Try it out"
4. Nhập JSON:
   ```json
   {
     "id": "001",
     "fullname": "Nguyễn Văn A"
   }
   ```
5. Click "Execute"

---

## ⚙️ Cấu Hình

### Cấu hình LED Display

File: `config/settings.yaml`

```yaml
led:
  rows: 32              # Số hàng
  cols: 64              # Số cột
  chain_length: 4       # Số module nối tiếp
  parallel: 2           # Số panel song song
  brightness: 70           # Độ sáng (0-100)
  hardware_mapping: regular  # ✅ Đã được kiểm tra và hoạt động
  gpio_slowdown: 4      # Thử 2-6 nếu có vấn đề
  font_path: /home/pi/rpi-rgb-led-matrix/fonts/10x20.bdf
  text_color: [255, 255, 255]  # Màu text (RGB)
  background_color: [0, 0, 0]  # Màu nền (RGB)
  hold_seconds: 8.0    # Thời gian hiển thị (giây)
```

### Cấu hình Audio

```yaml
audio:
  language: vi          # Ngôn ngữ (vi, en, ...)
  slow: false           # Phát chậm
  playback_command: ["mpg123", "-q"]  # Lệnh phát audio
  cache_dir: null       # Thư mục cache (null = tự động)
```

### Cấu hình Service

```yaml
service:
  host: 0.0.0.0         # Địa chỉ lắng nghe
  port: 8000            # Cổng
  reload: false         # Tự động reload (development)
```

---

## 📝 API Endpoints

### POST `/announce`

Gửi thông báo để hiển thị trên LED và phát audio.

**Request:**
```json
{
  "id": "001",
  "fullname": "Nguyễn Văn A"
}
```

**Response:**
```json
{
  "status": "queued",
  "id": "001",
  "fullname": "Nguyễn Văn A"
}
```

**Ví dụ:**
```bash
curl -X POST http://localhost:8000/announce \
  -H "Content-Type: application/json" \
  -d '{"id":"001","fullname":"Nguyễn Văn A"}'
```

---

### GET `/healthz`

Kiểm tra trạng thái dịch vụ.

**Response:**
```json
{
  "status": "ok"
}
```

**Ví dụ:**
```bash
curl http://localhost:8000/healthz
```

---

## 🔧 Tùy Chỉnh

### Thay Đổi Màu Text

Sửa trong `config/settings.yaml`:

```yaml
led:
  text_color: [255, 255, 0]  # Màu vàng
  # text_color: [255, 0, 0]    # Màu đỏ
  # text_color: [0, 255, 0]    # Màu xanh lá
  # text_color: [0, 0, 255]    # Màu xanh dương
```

### Thay Đổi Font

1. Tìm font trong `/home/pi/rpi-rgb-led-matrix/fonts/`
2. Sửa trong `config/settings.yaml`:

```yaml
led:
  font_path: /home/pi/rpi-rgb-led-matrix/fonts/12x22.bdf
```

**Các font có sẵn:**
- `4x6.bdf` - Nhỏ nhất
- `6x10.bdf` - Nhỏ
- `10x20.bdf` - Vừa (mặc định)
- `12x22.bdf` - Lớn
- `18x34.bdf` - Rất lớn

### Thay Đổi Độ Sáng

```yaml
led:
  brightness: 50   # Tối hơn
  brightness: 100  # Sáng nhất
```

### Thay Đổi Thời Gian Hiển Thị

```yaml
led:
  hold_seconds: 5.0   # 5 giây
  hold_seconds: 10.0  # 10 giây
```

---

## 🎯 Sử Dụng Trong Production

### Chạy với systemd (Tự động khởi động)

Tạo file service: `/etc/systemd/system/led-announcer.service`

```ini
[Unit]
Description=LED Announcer Service
After=network.target

[Service]
Type=simple
User=loaled
WorkingDirectory=/home/loaled/Desktop/loaled/led_announcer
Environment="PATH=/home/loaled/Desktop/loaled/led_announcer/.venv/bin"
ExecStart=/home/loaled/Desktop/loaled/led_announcer/.venv/bin/uvicorn src.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Các lệnh:**
```bash
# Tải service
sudo systemctl daemon-reload

# Khởi động
sudo systemctl start led-announcer

# Tự động khởi động khi boot
sudo systemctl enable led-announcer

# Xem log
sudo journalctl -u led-announcer -f

# Dừng
sudo systemctl stop led-announcer
```

---

## 🐛 Xử Lý Lỗi

### Lỗi: "Font file not found"

**Giải pháp:**
1. Kiểm tra font có tồn tại:
   ```bash
   ls -la /home/pi/rpi-rgb-led-matrix/fonts/
   ```
2. Cập nhật đường dẫn trong `config/settings.yaml`

---

### Lỗi: "LED display unavailable"

**Giải pháp:**
1. Kiểm tra kết nối phần cứng
2. Kiểm tra nguồn điện
3. Kiểm tra cấu hình `hardware_mapping`
4. Chạy với quyền root nếu cần:
   ```bash
   sudo uvicorn src.main:app --host 0.0.0.0 --port 8000
   ```

---

### Lỗi: Audio không phát

**Giải pháp:**
1. Kiểm tra `mpg123` đã cài đặt:
   ```bash
   which mpg123
   ```
2. Cài đặt nếu chưa có:
   ```bash
   sudo apt-get install mpg123
   ```
3. Kiểm tra loa/headphone đã kết nối

---

## 📚 Tài Liệu Tham Khảo

- `HUONG_DAN_TEST.md` - Hướng dẫn test màn hình
- `KHUAC_PHUC_LED_KHONG_SANG.md` - Khắc phục LED không sáng
- `KIEM_TRA_SO_DO_CHAN.md` - Kiểm tra sơ đồ chân GPIO
- `KET_NOI_HARDWARE.md` - Hướng dẫn kết nối phần cứng

---

## 🎉 Chúc Mừng!

LED Matrix của bạn đã hoạt động! Bây giờ bạn có thể:

1. ✅ Hiển thị text trên LED
2. ✅ Phát audio (nếu đã cấu hình)
3. ✅ Nhận thông báo qua API
4. ✅ Tích hợp với hệ thống khác

Chúc bạn sử dụng thành công! 🚀

