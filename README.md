# LED Announcer Service

Dịch vụ Python dành cho Raspberry Pi 4 nhằm nhận yêu cầu qua HTTP (ví dụ Postman), hiển thị họ tên trên màn hình LED P4 256x128 (module 2121 A2) và phát giọng nói tiếng Việt bằng Google Text-to-Speech.

## 📥 Cài đặt từ GitHub

### Yêu cầu hệ thống
- Raspberry Pi 4 (hoặc Pi 3/Zero 2 W)
- Raspberry Pi OS (Bullseye hoặc mới hơn)
- Kết nối internet
- Màn hình LED P4 256x128 2121 A2 và mạch điều khiển
- Loa (jack audio hoặc USB)

### Bước 1: Clone repository

```bash
cd ~
git clone https://github.com/TEN_USER/led-announcer.git
cd led-announcer
```

### Bước 2: Chạy script cài đặt tự động

```bash
chmod +x scripts/setup_from_git.sh
# Chế độ tự động (mặc định)
./scripts/setup_from_git.sh --auto

# Hoặc chỉ in hướng dẫn để tự thực hiện từng bước
./scripts/setup_from_git.sh --manual
```

Chế độ tự động sẽ đảm nhiệm:
- Cập nhật hệ thống và cài đặt package cần thiết (`python3-*`, `mpg123`, ...)
- Clone/ cập nhật và build `rpi-rgb-led-matrix`
- Tạo virtual environment
- Cài đặt các thư viện Python cần thiết và kiểm tra phụ thuộc

Chế độ `--manual` chỉ in ra danh sách bước thao tác tay để bạn tùy biến (ví dụ đổi thư mục, bỏ bớt bước), không thực thi bất cứ lệnh cài đặt nào.

### Bước 3: Kiểm tra phần cứng

```bash
# Test kết nối LED
python3 scripts/test_led_simple.py

# Test hiển thị text
python3 scripts/test_app.py
```

### Bước 4: Khởi động dịch vụ

```bash
# Chạy thủ công
source .venv/bin/activate
uvicorn src.main:app --host 0.0.0.0 --port 8000

# Hoặc dùng script
./scripts/start_service.sh
```

## 🚀 Sử dụng

### Test API

```bash
# Health check
curl http://localhost:8000/healthz

# Test announce
curl -X POST http://localhost:8000/announce \
  -H "Content-Type: application/json" \
  -d '{"id":"001","fullname":"Nguyễn Văn A"}'
```

### Từ thiết bị khác

```http
POST http://<IP_RASPBERRY_PI>:8000/announce
Content-Type: application/json

{
  "id": "123",
  "fullname": "Nguyễn Văn A"
}
```

## ⚙️ Cấu hình

Thay đổi thông số trong `config/settings.yaml`:

- `led`: kích thước panel, độ sáng, tốc độ PWM, đường dẫn font
- `audio`: ngôn ngữ TTS (mặc định `vi`), lệnh phát (`mpg123 -q`)
- `service`: địa chỉ và cổng chạy FastAPI

## 🛠️ Cài đặt thủ công (nếu script tự động thất bại)

### Cài đặt dependencies

```bash
# 1. Update hệ thống
sudo apt update && sudo apt upgrade -y

# 2. Cài đặt các package cần thiết
sudo apt install -y python3-pip python3-venv build-essential python3-dev git mpg123 curl cython3

# 3. Clone & cài đặt rpi-rgb-led-matrix
cd ~
git clone https://github.com/hzeller/rpi-rgb-led-matrix.git
cd rpi-rgb-led-matrix
make build-python
sudo make install-python

# 4. Quay lại thư mục dự án
cd ~/led-announcer

# 5. Tạo & kích hoạt virtualenv
python3 -m venv .venv
source .venv/bin/activate

# 6. Cài dependencies Python
pip install --upgrade pip
pip install -r requirements.txt

# 7. Cấp quyền chạy script (tuỳ chọn)
chmod +x scripts/*.sh scripts/*.py
```

## 🔧 Tạo service systemd (tuỳ chọn)

```bash
# Sao chép file service
sudo cp config/led-announcer.service /etc/systemd/system/

# Điều chỉnh đường dẫn nếu cần (nếu clone đến thư mục khác)
sudo nano /etc/systemd/system/led-announcer.service

# Kích hoạt service
sudo systemctl daemon-reload
sudo systemctl enable --now led-announcer.service

# Kiểm tra status
sudo systemctl status led-announcer
```

## 📖 Tài liệu tham khảo

- `HUONG_DAN_SU_DUNG.md` - Hướng dẫn sử dụng chi tiết
- `HUONG_DAN_TEST.md` - Hướng dẫn test màn hình
- `KET_NOI_HARDWARE.md` - Hướng dẫn kết nối phần cứng
- `KHUAC_PHUC_LED_KHONG_SANG.md` - Khắc phục LED không sáng


