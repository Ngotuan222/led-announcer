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

### 📢 Tăng max volume trên Raspberry Pi 4B

Mặc định loa trên Raspberry Pi 4B có thể không đủ lớn để nghe rõ trong môi trường ồn. Dưới đây là hướng dẫn tăng max volume bằng các lệnh amixer/alsamixer.

```bash
# 1) Tăng volume lên 100% cho card/thiết bị audio mặc định
amixer set Master 100%

# 2) Mở giao diện âm thanh để điều chỉnh
alsamixer

#  - Dùng phím mũi tên lên/xuống để tăng/giảm volume.
#  - Nhấn M để bật/tắt (khi phần trăm volume hiện là 0).
#  - Nhấn Esc để đóng cửa sổ.

# 3) Lưu lại cấu hình volume hiện tại
sudo alsactl store
```

Sau khi tăng volume, bạn cần khởi động lại dịch vụ để áp dụng thay đổi.

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

### 🔄 Khởi động lại (reset) service

- **Nếu dùng systemd** (đã tạo `led-announcer.service`):

  ```bash
  # Khởi động lại sau khi sửa code hoặc config
  sudo systemctl restart led-announcer

  # Xem log realtime để debug khi có lỗi
  sudo journalctl -u led-announcer -f
  ```

- **Nếu chạy thủ công bằng uvicorn** (không dùng systemd):

  ```bash
  # 1. Dừng tiến trình hiện tại (Ctrl + C trong terminal đang chạy uvicorn)

  # 2. Kích hoạt lại virtualenv (nếu cần)
  cd ~/led-announcer
  source .venv/bin/activate

  # 3. Chạy lại service
  uvicorn src.main:app --host 0.0.0.0 --port 8000
  ```

### ⏹️ Dừng hẳn service

- **Nếu dùng systemd**:

  ```bash
  # Dừng service và không chạy lại cho đến khi bạn start thủ công
  sudo systemctl stop led-announcer
  ```

- **Nếu chạy thủ công bằng uvicorn**:

  ```bash
  # Dừng service đang chạy trong terminal hiện tại
  Ctrl + C
  ```

## 📖 Tài liệu tham khảo

- `HUONG_DAN_SU_DUNG.md` - Hướng dẫn sử dụng chi tiết
- `HUONG_DAN_TEST.md` - Hướng dẫn test màn hình
- `KET_NOI_HARDWARE.md` - Hướng dẫn kết nối phần cứng
- `KHUAC_PHUC_LED_KHONG_SANG.md` - Khắc phục LED không sáng

## 🧾 Ghi chú cách cập nhật code lên GitHub (nhánh `master`)

Repository GitHub:

```bash
https://github.com/Ngotuan222/led-announcer.git
```

### 0. Cấu hình thông tin người dùng Git (làm một lần)

```bash
git config --global user.name "Ngotuan222"
git config --global user.email "ngohuutuan.vtn@gmail.com"   # Thay bằng email GitHub của bạn

# Kiểm tra lại thông tin đã cấu hình
git config --list | grep user
```

### 1. Kiểm tra trạng thái hiện tại

```bash
git status
git remote -v
```

- Đảm bảo đang ở đúng thư mục dự án:

```bash
cd ~/led-announcer
```

- Đảm bảo đang ở nhánh `master`:

```bash
git branch
# Nếu chưa ở master thì chuyển sang:
git checkout master
```

### 2. Thêm file và tạo commit mới

```bash
# Thêm tất cả thay đổi (hoặc thay bằng tên file cụ thể nếu muốn chọn lọc)
git add .
# Tạo commit với nội dung mô tả rõ ràng
git commit -m "Mo ta ngan gon ve thay doi"  # VD: "Cap nhat config panel 64x32"
```

Nếu Git báo "nothing to commit" nghĩa là chưa có thay đổi mới so với commit gần nhất.

### 3. Đẩy code lên GitHub (nhánh `master`)

```bash
git push origin master
```

Sau khi chạy lệnh trên, vào trang:

```bash
https://github.com/Ngotuan222/led-announcer
```

để kiểm tra lại code đã được cập nhật.

## 🧾 Ghi chú cấu hình panel 64x32 ICN2012

- **Phần cứng**
  - Panel P5 64x32, driver ICN2012.
  - Cấu hình cơ bản trong `config/settings.yaml`:
    - `rows: 32`, `cols: 64`, `chain_length: 1`, `parallel: 1`.
- **Multiplexing**
  - Panel hiển thị lặp 3 lần theo chiều dọc nếu dùng cấu hình mặc định.
  - Đã khắc phục bằng cách thêm trường `multiplexing`:
    - Trong `config/settings.yaml`:
      - `multiplexing: 1`.
    - Trong `src/config.py` (`LedDisplayConfig`):
      - Thêm thuộc tính `multiplexing: int = 0`.
    - Trong `src/display.py` (`LedDisplay._build_options`):
      - `options.multiplexing = self.config.multiplexing`.
- **Font & căn giữa text**
  - Đường dẫn font hiện tại trong `settings.yaml`:
    - `font_path: /home/loaled/rpi-rgb-led-matrix/fonts/7x13.bdf`.
  - Các hàm hiển thị text sử dụng cấu hình từ `LedDisplayConfig`:
    - `LedDisplay.show_text()` – text tĩnh căn giữa theo chiều ngang, baseline được dời lên một chút để không chạm mép dướ
    - `LedDisplay.show_scrolling_text()` – hiển thị 2 dòng (tên cũ + tên mới), đối xứng quanh tâm màn hình, mỗi dòng có baseline được dịch lên để phù hợp panel 64x32.
- **Script test riêng cho panel 64x32**
  - `testled/testled.py` (ngoài project `led-announcer`):
    - Cấu hình cố định 64x32, `multiplexing = 1`.
    - Vẽ một điểm tâm màn hình và chữ "test" căn giữa để kiểm tra nhanh mapping phần cứng.

## 🧪 Ghi chú sự cố & khắc phục GPIO 5 (door control)

### Triệu chứng

- API `/announce` trả về:
  - `{ "status": "ok", "door_status": "open-door" }` hoặc `"close-door"`.
- Nhưng khi đo chân **GPIO5 (BCM 5, chân vật lý 29)** trên Raspberry Pi 4B:
  - Không thấy điện áp thay đổi khi gọi `open-door` / `close-door`.

### Nguyên nhân gốc

1. **RPi.GPIO chưa được cài trong virtualenv** mà service systemd sử dụng:
   - Service `led-announcer` chạy với:
     - `WorkingDirectory=/home/loaled/Desktop/loaled/led-announcer`
     - `PATH=/home/loaled/Desktop/loaled/led-announcer/.venv/bin:...`
     - `ExecStart=/home/loaled/Desktop/loaled/led-announcer/.venv/bin/uvicorn src.main:app ...`
   - Trong log `journalctl -u led-announcer` có dòng cảnh báo:
     - `RPi.GPIO not available. Door control GPIO26 will be disabled.`
   - Khi đó, hàm `_handle_door_status()` trong `src/main.py` chỉ log cảnh báo và **không gọi** `GPIO.output(...)`, nhưng API vẫn trả `door_status`.

2. Ban đầu door control dùng **BCM 26** nên có nguy cơ trùng với mapping HUB75 của `rpi-rgb-led-matrix`. Sau đó đã đổi sang **BCM 5** để hoàn toàn tách biệt với chân LED.

### Cách khắc phục

1. **Cài RPi.GPIO trong đúng virtualenv** mà service dùng:

   ```bash
   cd /home/loaled/Desktop/loaled/led-announcer
   source .venv/bin/activate
   pip install RPi.GPIO
   deactivate
   ```

2. **Khởi động lại service** để dùng môi trường mới:

   ```bash
   sudo systemctl restart led-announcer
   sudo journalctl -u led-announcer -n 20
   ```

   - Đảm bảo log **không còn** dòng `RPi.GPIO not available...`.

3. **Xác nhận door control dùng đúng chân GPIO5 (pin 29)**:

   - Trong `src/main.py`:

     ```python
     GPIO.setmode(GPIO.BCM)
     DOOR_GPIO_PIN = 5  # GPIO5 (BCM), chân vật lý 29
     ```

   - Trong `KET_NOI_HARDWARE.md` có bảng `BCM ↔ chân vật lý`, trong đó:
     - `5 | 29 | GPIO5 – dùng cho điều khiển cửa (door control) trong code`.

4. **Test trực tiếp GPIO5 bằng script Python đơn giản** (để loại trừ vấn đề phần cứng/đấu dây):

   ```bash
   python3 - << 'EOF'
   import RPi.GPIO as GPIO
   import time

   PIN = 5  # BCM5, chân vật lý 29
   GPIO.setmode(GPIO.BCM)
   GPIO.setup(PIN, GPIO.OUT, initial=GPIO.LOW)

   print("LOW  (0V)..."); time.sleep(3)
   GPIO.output(PIN, GPIO.HIGH)
   print("HIGH (~3.3V)..."); time.sleep(10)
   GPIO.output(PIN, GPIO.LOW)
   print("LOW again"); time.sleep(3)

   GPIO.cleanup(PIN)
   EOF
   ```

5. **Test lại qua API**:

   ```bash
   curl -X POST http://localhost:8000/announce \
     -u admin:hkqt@2024 \
     -H "Content-Type: application/json" \
     -d '{"status": "open-door"}'

   curl -X POST http://localhost:8000/announce \
     -u admin:hkqt@2024 \
     -H "Content-Type: application/json" \
     -d '{"status": "close-door"}'
   ```

   - Khi service chạy đúng, điện áp trên chân **pin 29** sẽ lần lượt **lên HIGH (~3.3V)** rồi về **LOW (0V)**.
