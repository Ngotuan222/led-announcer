# Khắc Phục Lỗi Kết Nối ECONNREFUSED

## ⚠️ Lỗi: `Error: connect ECONNREFUSED 127.0.0.1:8000`

Lỗi này có nghĩa là client không thể kết nối đến dịch vụ trên port 8000.

## 🔍 Kiểm Tra

### 1. Kiểm tra dịch vụ có đang chạy không

```bash
# Kiểm tra process
ps aux | grep uvicorn | grep -v grep

# Kiểm tra port
netstat -tuln | grep 8000
# hoặc
ss -tuln | grep 8000
```

**Kết quả mong đợi:**
- Process uvicorn đang chạy
- Port 8000 đang được lắng nghe (LISTEN)

---

### 2. Test kết nối từ localhost

```bash
# Test health check
curl http://127.0.0.1:8000/healthz

# Test với POST request
curl -X POST http://127.0.0.1:8000/announce \
  -H "Content-Type: application/json" \
  -d '{"id":"test","fullname":"Test LED"}'
```

**Nếu curl thành công:** Dịch vụ đang hoạt động, vấn đề có thể ở client.

**Nếu curl thất bại:** Dịch vụ có vấn đề, xem phần "Khởi Động Dịch Vụ" bên dưới.

---

### 3. Kiểm tra firewall

```bash
# Kiểm tra firewall có chặn port 8000 không
sudo ufw status
# hoặc
sudo iptables -L -n | grep 8000
```

**Nếu firewall đang chặn:**
```bash
# Mở port 8000 (nếu dùng ufw)
sudo ufw allow 8000/tcp
```

---

## 🚀 Khởi Động Dịch Vụ

### Cách 1: Chạy trực tiếp

```bash
cd /home/loaled/Desktop/loaled/led_announcer
source .venv/bin/activate
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

**Lưu ý:**
- `--host 0.0.0.0` cho phép kết nối từ mọi interface
- `--host 127.0.0.1` chỉ cho phép kết nối từ localhost

---

### Cách 2: Chạy trong background

```bash
cd /home/loaled/Desktop/loaled/led_announcer
source .venv/bin/activate
nohup uvicorn src.main:app --host 0.0.0.0 --port 8000 > /tmp/led-announcer.log 2>&1 &
```

**Kiểm tra log:**
```bash
tail -f /tmp/led-announcer.log
```

---

### Cách 3: Chạy với systemd (Production)

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

# Kiểm tra trạng thái
sudo systemctl status led-announcer

# Dừng
sudo systemctl stop led-announcer
```

---

## 🔧 Các Vấn Đề Thường Gặp

### Vấn đề 1: Dịch vụ crash khi khởi động

**Nguyên nhân:**
- Lỗi khởi tạo LED display
- Font file không tìm thấy
- Cấu hình sai

**Giải pháp:**
1. Kiểm tra log:
   ```bash
   tail -f /tmp/led-announcer.log
   # hoặc
   sudo journalctl -u led-announcer -f
   ```

2. Test LED display trước:
   ```bash
   python3 scripts/test_app.py
   ```

3. Kiểm tra font file:
   ```bash
   ls -la /home/loaled/rpi-rgb-led-matrix/fonts/10x20.bdf
   ```

---

### Vấn đề 2: Kết nối từ máy khác bị từ chối

**Nguyên nhân:**
- Dịch vụ chỉ lắng nghe trên 127.0.0.1
- Firewall chặn
- Network không cho phép

**Giải pháp:**
1. Khởi động với `--host 0.0.0.0`:
   ```bash
   uvicorn src.main:app --host 0.0.0.0 --port 8000
   ```

2. Kiểm tra firewall:
   ```bash
   sudo ufw allow 8000/tcp
   ```

3. Kiểm tra IP của server:
   ```bash
   hostname -I
   ```

4. Test từ máy khác:
   ```bash
   curl http://<IP_SERVER>:8000/healthz
   ```

---

### Vấn đề 3: Port 8000 đã được sử dụng

**Nguyên nhân:**
- Dịch vụ khác đang dùng port 8000
- Dịch vụ cũ chưa dừng

**Giải pháp:**
1. Tìm process đang dùng port:
   ```bash
   sudo lsof -i :8000
   # hoặc
   sudo fuser 8000/tcp
   ```

2. Dừng process:
   ```bash
   # Tìm PID từ lệnh trên
   kill <PID>
   # hoặc force kill
   kill -9 <PID>
   ```

3. Hoặc đổi port trong config:
   ```yaml
   service:
     port: 8001  # Đổi port khác
   ```

---

### Vấn đề 4: IPv6 vs IPv4

**Nguyên nhân:**
- Client đang dùng IPv6 (::1) nhưng dịch vụ chỉ lắng nghe IPv4

**Giải pháp:**
1. Dùng IPv4 trong client:
   ```bash
   # Thay vì localhost, dùng 127.0.0.1
   curl http://127.0.0.1:8000/healthz
   ```

2. Hoặc khởi động dịch vụ với IPv6:
   ```bash
   uvicorn src.main:app --host :: --port 8000
   ```

---

## 📋 Checklist

Trước khi báo lỗi, đảm bảo:

- [ ] Dịch vụ đang chạy (`ps aux | grep uvicorn`)
- [ ] Port 8000 đang được lắng nghe (`netstat -tuln | grep 8000`)
- [ ] Test với curl từ localhost thành công
- [ ] Firewall không chặn port 8000
- [ ] Dịch vụ khởi động với `--host 0.0.0.0` (nếu cần kết nối từ xa)
- [ ] Không có process khác đang dùng port 8000

---

## 🆘 Nếu Vẫn Không Hoạt Động

1. **Kiểm tra log chi tiết:**
   ```bash
   # Chạy dịch vụ ở foreground để xem log
   cd /home/loaled/Desktop/loaled/led_announcer
   source .venv/bin/activate
   uvicorn src.main:app --host 0.0.0.0 --port 8000 --log-level debug
   ```

2. **Test từng bước:**
   ```bash
   # Test health check
   curl http://127.0.0.1:8000/healthz
   
   # Test với IPv4
   curl http://127.0.0.1:8000/healthz
   
   # Test với IPv6
   curl http://[::1]:8000/healthz
   ```

3. **Kiểm tra network:**
   ```bash
   # Kiểm tra interface
   ip addr show
   
   # Kiểm tra routing
   ip route show
   ```

---

## 📚 Tài Liệu Tham Khảo

- `HUONG_DAN_SU_DUNG.md` - Hướng dẫn sử dụng
- `HUONG_DAN_TEST.md` - Hướng dẫn test

