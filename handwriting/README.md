# 📖 GuestBook — Sổ Lưu Bút Trực Tuyến

Ứng dụng web **Guestbook** đơn giản xây dựng bằng **Flask (Python)**, cho phép khách ghé thăm để lại lời nhắn, xem danh sách lời nhắn, xóa lời nhắn và xem thống kê trực quan bằng biểu đồ Matplotlib.

---

## 🗂️ Cấu trúc Project

```
BTPY/
├── app.py                  # Flask backend — toàn bộ routes & logic
├── data.json               # Lưu trữ lời nhắn (tự tạo khi chạy)
├── requirements.txt        # Danh sách thư viện cần cài
├── templates/
│   ├── base.html           # Layout chung (navbar, flash messages, footer)
│   ├── index.html          # Trang chủ — hiển thị danh sách lời nhắn
│   ├── add.html            # Form gửi lời nhắn mới
│   └── stats.html          # Trang thống kê + biểu đồ cột
└── static/
    ├── css/
    │   └── style.css       # Giao diện Dark mode / Glassmorphism
    └── js/
        └── main.js         # Animations, char counter, confirm xoá
```

---

## ⚙️ Yêu cầu hệ thống

| Công cụ | Phiên bản tối thiểu |
|---------|---------------------|
| Python  | 3.9+                |
| Flask   | 2.3+                |
| Matplotlib | 3.7+            |

---

## 🚀 Cài đặt & Chạy

### 1. Clone hoặc tải project về máy

```bash
cd c:\Users\ADM\Desktop\BTPY
```

### 2. Cài đặt thư viện

```bash
pip install -r requirements.txt
```

Hoặc cài thủ công:

```bash
pip install flask matplotlib
```

### 3. Chạy ứng dụng

```bash
python app.py
```

### 4. Mở trình duyệt

```
http://127.0.0.1:5000
```

---

## 📌 Các Route (Endpoints)

### Buổi 1 — Routes cơ bản

| Route | Method | Mô tả |
|-------|--------|-------|
| `/` | GET | Hiển thị tất cả lời nhắn (mới nhất lên đầu) |
| `/add` | GET | Hiển thị form nhập **tên** và **lời nhắn** |
| `/add` | POST | Validate → lưu vào JSON → redirect về `/`; nếu lỗi render lại form với thông báo |
| `/delete/<id>` | GET/POST | Xóa lời nhắn theo ID → redirect về `/` |

**Quy tắc validate `/add` POST:**
- Cả hai trường `name` và `message` đều **bắt buộc** nhập.
- Nếu thiếu trường nào → render lại form kèm thông báo lỗi cụ thể.

---

### Buổi 2 — Lưu trữ & Thống kê

| Route | Method | Mô tả |
|-------|--------|-------|
| `/stats` | GET | Tổng số lời nhắn, Top 5 người gửi nhiều nhất, biểu đồ cột Matplotlib |

**Lưu trữ dữ liệu:**
- Khi khởi động: đọc `data.json` (nếu có).
- Khi thêm / xóa: ghi lại `data.json` → **dữ liệu không mất khi tắt chương trình**.

**Biểu đồ:**
- Vẽ bằng **Matplotlib**, lưu tạm thành `static/stats.png`.
- Nhúng vào HTML dưới dạng **Base64** (không cần serve file tĩnh riêng).

---

## 🗃️ Cấu trúc dữ liệu (`data.json`)

```json
[
  {
    "id": 1,
    "name": "Nguyen Van A",
    "message": "Trang web rat dep!",
    "timestamp": "20/10/2024 09:00"
  },
  {
    "id": 2,
    "name": "Tran Thi B",
    "message": "Chuc mung ngay moi!",
    "timestamp": "20/10/2024 09:15"
  }
]
```

---

## 🎨 Giao diện

- **Dark mode** với nền `#080C14` và các lớp glassmorphism.
- **Màu chủ đạo:** Gradient tím `#6C63FF` → hồng `#EC4899`.
- **Font:** [Inter](https://fonts.google.com/specimen/Inter) (Google Fonts).
- **Responsive** — hỗ trợ mobile, tablet, desktop.
- **Micro-animations:** entry card hover, fade-in, thanh leaderboard animated.

---

## 📊 Trang Thống Kê (`/stats`)

- **Tổng số lời nhắn** đã ghi.
- **Top 5 người gửi** nhiều lời nhắn nhất (dùng `collections.Counter`).
- **Biểu đồ cột (bar chart)** minh họa số lượng lời nhắn theo người gửi (Matplotlib).

---

## 🧩 Công nghệ sử dụng

| Thành phần | Công nghệ |
|------------|-----------|
| Backend | Python 3 + Flask |
| Template | Jinja2 (HTML thuần) |
| Styling | Vanilla CSS (Dark mode, Glassmorphism) |
| JS | Vanilla JavaScript (ES5+) |
| Biểu đồ | Matplotlib |
| Lưu trữ | JSON file (`data.json`) |

---

## 👥 Phân loại theo buổi học

### Buổi 1 — HTML thuần + Routes cơ bản
- Route `GET /` — lấy danh sách và render `index.html` với biến `entries`.
- Route `GET /add` — hiển thị form.
- Route `POST /add` — validate, lưu vào list Python, redirect.
- Route `GET|POST /delete/<int:id>` — xóa entry, redirect.

### Buổi 2 — Web & Đồ thị
- Lưu/tải dữ liệu từ `data.json`.
- Route `GET /stats` — thống kê tổng số, Top 5, biểu đồ cột Matplotlib.

---

## 📝 Ghi chú

- File `data.json` được tạo tự động nếu chưa tồn tại.
- Ứng dụng chạy ở chế độ **debug** (chỉ dùng cho phát triển).
- ID của lời nhắn là **tự tăng an toàn** — không bị trùng kể cả sau khi xóa.

---

*Xây dựng bằng Flask & Python — Manual Code Version* 🐍
