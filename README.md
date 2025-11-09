# LED Announcer Service

Dịch vụ Python dành cho Raspberry Pi 4 nhằm nhận yêu cầu qua HTTP (ví dụ Postman), hiển thị họ tên trên màn hình LED P4 256x128 (module 2121 A2) và phát giọng nói tiếng Việt bằng Google Text-to-Speech.

## Chức năng chính

- API `POST /announce` nhận JSON gồm `id` và `fullname`.
- Tên (`fullname`) được đưa lên LED matrix thông qua thư viện `rpi-rgb-led-matrix`.
- Dùng Google TTS (`gTTS`) để phát âm thanh tiếng Việt (qua `mpg123`).
- API `GET /healthz` để kiểm tra tình trạng dịch vụ.

## Yêu cầu phần cứng

- Raspberry Pi 4.
- Màn hình LED P4 256x128 2121 A2 và mạch điều khiển tương thích (ví dụ Adafruit RGB Matrix HAT).
- Loa kết nối với jack audio hoặc qua USB.

## Chuẩn bị hệ thống

```bash
cd /home/loaled/Desktop/loaled/led_announcer
chmod +x scripts/install_dependencies.sh
./scripts/install_dependencies.sh
```

Ghi chú:

- Script trên cài `mpg123` để phát file MP3.
- **Cài đặt rpi-rgb-led-matrix:**
  ```bash
  ./scripts/install_rgb_matrix.sh
  ```
  Script này sẽ tự động clone, build và cài đặt thư viện cùng Python bindings.
  
  Hoặc cài đặt thủ công:
  ```bash
  cd ~
  git clone https://github.com/hzeller/rpi-rgb-led-matrix.git
  cd rpi-rgb-led-matrix
  make build-python
  sudo make install-python
  ```
- Font mặc định tham chiếu tới `/home/pi/rpi-rgb-led-matrix/fonts/10x20.bdf`. Điều chỉnh đường dẫn trong `config/settings.yaml` nếu cần.

## Cấu hình

Thay đổi thông số trong `config/settings.yaml`:

- `led`: kích thước panel, độ sáng, tốc độ PWM, đường dẫn font.
- `audio`: ngôn ngữ TTS (mặc định `vi`), lệnh phát (`mpg123 -q`).
- `service`: địa chỉ và cổng chạy FastAPI.

## Chạy dịch vụ

### Cách 1: Sử dụng script (Khuyến nghị)

```bash
./scripts/start_service.sh
```

Script này sẽ tự động:
- Kiểm tra và dừng process cũ nếu port đang được sử dụng
- Kích hoạt virtual environment
- Khởi động dịch vụ

### Cách 2: Chạy thủ công

```bash
source .venv/bin/activate
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

### Dừng dịch vụ

Nếu port bị chiếm, dừng process cũ:
```bash
./scripts/stop_service.sh
```

Hoặc tìm và dừng thủ công:
```bash
lsof -ti :8000 | xargs kill
```

Truy cập từ thiết bị khác (ví dụ Postman):

```http
POST http://<IP_RASPBERRY_PI>:8000/announce
Content-Type: application/json

{
  "id": "123",
  "fullname": "Nguyễn Văn A"
}
```

## Tạo service systemd (tuỳ chọn)

1. Sao chép file mẫu:

```bash
sudo cp config/led-announcer.service /etc/systemd/system/
```

2. Điều chỉnh đường dẫn người dùng, virtualenv trong file nếu khác.

3. Nạp và khởi động:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now led-announcer.service
```

## Kiểm thử nhanh

```bash
curl -X POST http://localhost:8000/announce \
  -H "Content-Type: application/json" \
  -d '{"id":"42","fullname":"Trần Thị B"}'
```

Nếu phần LED chưa sẵn sàng, dịch vụ vẫn phát TTS và ghi log cảnh báo. Khi phần cứng hoạt động, gói tin tiếp theo sẽ hiển thị đầy đủ.


