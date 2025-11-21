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

## 📝 Ghi chú cấu hình panel 64x32 ICN2012

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
