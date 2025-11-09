# LED Announcer Service

Dịch vụ Python dành cho Raspberry Pi 4 nhằm nhận yêu cầu qua HTTP (ví dụ Postman), hiển thị họ tên trên màn hình LED P4 256x128 (module 2121 A2) và phát giọng nói tiếng Việt bằng Google Text-to-Speech.

## 📥 Cài đặt từ Git

### Yêu cầu hệ thống
- Raspberry Pi 4 (hoặc Pi 3/Zero 2 W)
- Raspberry Pi OS (Bullseye hoặc mới hơn)
- Kết nối internet
- Màn hình LED P4 256x128 2121 A2 và mạch điều khiển
- Loa (jack audio hoặc USB)

### Bước 1: Clone repository

```bash
cd ~
git clone <URL_REPOSITORY_GIT_CUA_BAN>
cd led_announcer
```

### Bước 2: Chạy script cài đặt tự động

```bash
chmod +x scripts/setup_from_git.sh
./scripts/setup_from_git.sh
```

Script này sẽ tự động:
- Cài đặt Python dependencies
- Cài đặt `mpg123` cho audio
- Clone và cài đặt `rpi-rgb-led-matrix`
- Tạo virtual environment
- Cài đặt các thư viện Python cần thiết

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
# Update system
sudo apt update && sudo apt upgrade -y

# Cài đặt các package cần thiết
sudo apt install -y python3-pip python3-venv build-essential python3-dev git mpg123

# Clone và cài đặt rpi-rgb-led-matrix
cd ~
git clone https://github.com/hzeller/rpi-rgb-led-matrix.git
cd rpi-rgb-led-matrix
make build-python
sudo make install-python
cd ~/led_announcer

# Tạo và kích hoạt virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Cài đặt Python dependencies
pip install -r requirements.txt
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


