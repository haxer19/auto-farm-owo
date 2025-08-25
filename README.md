# Hướng Dẫn Cài Đặt & Chạy Self-Bot

⚠️ **Lưu ý quan trọng**: Self-bot chỉ hỗ trợ **Python 3.11**, các phiên bản khác sẽ không chạy được.

---

## 1. Tải Python 3.11
1. Vào trang chính thức của Python: [https://www.python.org/downloads/release/python-3110/](https://www.python.org/downloads/release/python-3110/)
2. Chọn phiên bản phù hợp với hệ điều hành của bạn:
   - **Windows**: tải file `.exe` (Installer)
   - **Linux/MacOS**: có thể dùng `apt`, `brew` hoặc tải source
3. Trong quá trình cài đặt:
   - Đánh dấu chọn **Add Python 3.11 to PATH**
   - Sau đó bấm **Install Now**

Kiểm tra cài đặt bằng cách mở **Terminal/CMD** và chạy:
```bash
python --version
````

hoặc

```bash
python3 --version
```

Kết quả phải hiển thị `Python 3.11.x`.

---

## 2. Cài Thư Viện Yêu Cầu

Trong thư mục dự án, chạy lệnh:

```bash
pip install -r requirements.txt
```

Nội dung file `requirements.txt`:

```
git+https://github.com/dolfies/discord.py-self.git
colorama
```

---

## 3. Chạy File main.py

Sau khi cài đặt xong thư viện, bạn có thể chạy bot bằng:

```bash
python main.py
```

hoặc

```bash
python3 main.py
```

## 4. Lỗi Thường Gặp

* **Sai phiên bản Python**: Kiểm tra lại bằng `python --version`
* **pip không hoạt động**: Dùng `python -m pip install -r requirements.txt`
* **Thiếu thư viện**: Kiểm tra lại `requirements.txt` và cài lại
