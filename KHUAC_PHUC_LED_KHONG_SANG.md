# Khắc Phục LED Không Sáng

## ⚠️ Vấn Đề: Phần mềm chạy thành công nhưng không thấy LED sáng

Nếu script test chạy thành công (không có lỗi) nhưng bạn **KHÔNG thấy đèn LED sáng**, vấn đề nằm ở **phần cứng hoặc cấu hình**.

## 🔍 Kiểm Tra Từng Bước

### Bước 1: Kiểm Tra Nguồn Điện (QUAN TRỌNG NHẤT)

**Module LED phải có nguồn 5V riêng, không dùng nguồn từ Raspberry Pi!**

- [ ] **Module LED có đèn LED nguồn sáng không?**
  - Tìm đèn LED nhỏ trên module (thường màu đỏ hoặc xanh)
  - Nếu không có đèn sáng → **nguồn chưa được cấp hoặc sai cực tính**
  
- [ ] **Nguồn 5V đã được cấp chưa?**
  - Kiểm tra adapter nguồn 5V đã cắm và bật chưa
  - Nguồn phải đủ công suất: **2-4A cho 1 module**, **4-8A cho 2 module**
  - Đo điện áp: phải đúng 5V (không quá 5.5V, không dưới 4.5V)

- [ ] **Cực tính nguồn đúng chưa?**
  - **VCC (5V) → VCC** trên module
  - **GND → GND** trên module
  - ⚠️ **CỰC TÍNH SAI SẼ HỎNG MODULE!**
  - Kiểm tra kỹ trước khi cấp điện

---

### Bước 2: Kiểm Tra Cáp Dữ Liệu

- [ ] **Cáp IDC 16-pin đã được cắm?**
  - Một đầu: GPIO Raspberry Pi (hoặc HAT nếu có)
  - Đầu kia: Cổng **DATA_IN** trên module LED (KHÔNG phải DATA_OUT)

- [ ] **Cáp đã cắm chắc chắn?**
  - Kiểm tra xem cáp có bị lỏng không
  - Thử rút ra và cắm lại chắc chắn
  - Kiểm tra các chân không bị cong, gãy

- [ ] **Cáp đã cắm đúng chiều?**
  - Cáp IDC có rãnh định hướng (key)
  - Đảm bảo cắm đúng chiều, không ngược
  - Nếu cắm ngược có thể gây hỏng module

---

### Bước 3: Kiểm Tra GPIO (Nếu kết nối trực tiếp)

- [ ] **Đã kết nối đúng theo sơ đồ HUB-75E?**
  - Xem sơ đồ chi tiết trong `KIEM_TRA_SO_DO_CHAN.md`
  - Kiểm tra từng chân:
    - **R1, G1, B1, R2, G2, B2** (màu)
    - **A, B, C, D, E** (địa chỉ)
    - **CLK, LAT, OE** (điều khiển)
    - **GND** (nối đất - 2 chân: chân 4 và chân 16)

- [ ] **Không có chân nào bị chạm nhau?**
  - Kiểm tra xem các dây có bị chạm nhau không
  - Kiểm tra các chân GPIO không bị chạm nhau trên breadboard

- [ ] **Sơ đồ chân trên PCB module có khớp không?**
  - Xem sơ đồ chân **IN TRÊN PCB** của module LED
  - So sánh với sơ đồ trong `KIEM_TRA_SO_DO_CHAN.md`
  - Nếu khác, có thể cần thử hardware mapping khác

---

### Bước 4: Kiểm Tra Cấu Hình

- [ ] **Cấu hình có đúng với module LED của bạn không?**
  - Xem file `config/settings.yaml`
  - Kiểm tra:
    - `rows`: Số hàng của module (thường 32 hoặc 64)
    - `cols`: Số cột của module (thường 64 hoặc 128)
    - `chain_length`: Số module nối tiếp (1, 2, 4, ...)
    - `parallel`: Số panel song song (1, 2, ...)
    - `hardware_mapping`: `regular` (đã được kiểm tra)

- [ ] **Thử với cấu hình tối thiểu:**
  ```yaml
  led:
    rows: 32
    cols: 64
    chain_length: 1
    parallel: 1
    hardware_mapping: regular
    gpio_slowdown: 4
    brightness: 100
  ```

---

### Bước 5: Thứ Tự Bật Nguồn

**Thứ tự đúng:**
1. **Bật nguồn cho module LED TRƯỚC**
2. **Sau đó mới bật Raspberry Pi**

**Thứ tự sai có thể gây lỗi!**

---

## 🧪 Test Chi Tiết

### Test 1: Test với màu sáng rõ ràng

```bash
cd /home/loaled/Desktop/loaled/led_announcer
sudo .venv/bin/python3 scripts/test_led_bright.py
```

Script này sẽ:
- Hiển thị màu trắng (10 giây) - sáng nhất
- Hiển thị màu đỏ (5 giây)
- Hiển thị màu xanh lá (5 giây)
- Hiển thị màu xanh dương (5 giây)
- Hiển thị màu vàng (5 giây)

**Quan sát:** Bạn có thấy màn hình sáng với bất kỳ màu nào không?

---

### Test 2: Test với nhiều hardware mapping

Nếu không thấy đèn sáng, thử tất cả các hardware mapping:

```bash
cd /home/loaled/Desktop/loaled/led_announcer
sudo .venv/bin/python3 scripts/test_gpio_direct.py
```

Script này sẽ thử lần lượt:
- `regular` (đã được kiểm tra)
- `regular-pi1`
- `classic`
- `classic-pi1`
- `adafruit-hat`
- `adafruit-hat-pwm`

**Với mỗi mapping, script sẽ hỏi bạn có thấy đèn sáng không.**

---

### Test 3: Kiểm tra sơ đồ chân

```bash
cd /home/loaled/Desktop/loaled/led_announcer
python3 scripts/check_pinout.py
```

So sánh sơ đồ hiển thị với sơ đồ **IN TRÊN PCB** của module LED.

---

## 🔧 Các Vấn Đề Thường Gặp

### Vấn đề 1: Module LED không có đèn nguồn sáng

**Nguyên nhân:**
- Nguồn chưa được cấp
- Cực tính sai
- Nguồn không đủ điện áp

**Giải pháp:**
1. Kiểm tra adapter nguồn đã cắm và bật chưa
2. Kiểm tra cực tính: VCC → VCC, GND → GND
3. Đo điện áp: phải đúng 5V
4. Thử nguồn khác

---

### Vấn đề 2: Cáp dữ liệu chưa kết nối đúng

**Nguyên nhân:**
- Cáp chưa cắm
- Cắm vào cổng sai (DATA_OUT thay vì DATA_IN)
- Cáp bị lỏng
- Cáp cắm ngược

**Giải pháp:**
1. Kiểm tra cáp đã cắm vào cổng **DATA_IN** chưa
2. Rút ra và cắm lại chắc chắn
3. Kiểm tra cáp cắm đúng chiều (rãnh định hướng)
4. Thử cáp khác nếu có

---

### Vấn đề 3: Sơ đồ chân GPIO không đúng

**Nguyên nhân:**
- Sơ đồ chân trên PCB module khác với sơ đồ đã kiểm tra
- Kết nối GPIO sai
- Hardware mapping không phù hợp

**Giải pháp:**
1. Xem sơ đồ chân **IN TRÊN PCB** của module LED
2. So sánh với sơ đồ trong `KIEM_TRA_SO_DO_CHAN.md`
3. Thử test với nhiều hardware mapping (Test 2)
4. Nếu sơ đồ khác, có thể cần tạo custom hardware mapping

---

### Vấn đề 4: Cấu hình không đúng

**Nguyên nhân:**
- `rows`, `cols`, `chain_length`, `parallel` không đúng với module
- `hardware_mapping` không phù hợp

**Giải pháp:**
1. Kiểm tra thông số module LED của bạn
2. Cập nhật `config/settings.yaml` cho đúng
3. Thử với cấu hình tối thiểu (32x64, chain=1, parallel=1)

---

## 📋 Checklist Tổng Hợp

Trước khi báo lỗi, đảm bảo đã kiểm tra:

- [ ] Module LED có đèn LED nguồn sáng
- [ ] Nguồn 5V đã được cấp (đủ công suất)
- [ ] Cực tính nguồn đúng (VCC → VCC, GND → GND)
- [ ] Cáp IDC 16-pin đã cắm vào cổng DATA_IN
- [ ] Cáp đã cắm chắc chắn và đúng chiều
- [ ] Các chân GPIO đã kết nối đúng theo sơ đồ
- [ ] Không có chân nào bị chạm nhau
- [ ] Cấu hình `rows`, `cols`, `chain_length`, `parallel` đúng
- [ ] Đã thử với nhiều hardware mapping
- [ ] Đã bật nguồn module LED TRƯỚC khi bật Raspberry Pi

---

## 🆘 Nếu Vẫn Không Hoạt Động

Nếu đã kiểm tra tất cả các bước trên nhưng vẫn không thấy đèn sáng:

1. **Chụp ảnh:**
   - Sơ đồ chân trên PCB của module LED
   - Kết nối GPIO thực tế
   - Module LED (để xem model)

2. **Cung cấp thông tin:**
   - Model module LED (nếu có)
   - Sơ đồ chân trên PCB (ghi lại từng chân)
   - Kết nối GPIO thực tế (chân nào nối với GPIO nào)
   - Module LED có đèn LED nguồn sáng không?
   - Cáp IDC đã cắm đúng chiều chưa?

3. **Thử các giải pháp khác:**
   - Thử module LED khác (nếu có)
   - Thử cáp IDC khác
   - Thử nguồn khác
   - Thử HAT thay vì kết nối trực tiếp

---

## 📚 Tài Liệu Tham Khảo

- `KIEM_TRA_SO_DO_CHAN.md` - Kiểm tra sơ đồ chân GPIO
- `KET_NOI_HARDWARE.md` - Hướng dẫn kết nối phần cứng
- `KIEM_TRA_PHAN_CUNG.md` - Checklist kiểm tra phần cứng
- `HUONG_DAN_TEST.md` - Hướng dẫn test màn hình

