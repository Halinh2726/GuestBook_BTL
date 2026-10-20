# Dấu Ấn — Guestbook (Vibe Coding Version)

Phiên bản guestbook được thiết kế lại theo phong cách editorial hiện đại: giao diện sáng/tối, responsive, tìm kiếm lời nhắn, xem trước khi gửi và trang thống kê đồng bộ về hình ảnh.

## Chạy ứng dụng

```bash
cd vibe-coding
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Mở `http://127.0.0.1:5001`.

## Tính năng

- Thêm và xóa lời nhắn; dữ liệu lưu bền vững trong `data.json`.
- Validate dữ liệu ở cả trình duyệt và Flask.
- Tìm kiếm không phân biệt dấu tiếng Việt.
- Xem trước lời nhắn theo thời gian thực.
- Light/dark mode và ghi nhớ lựa chọn.
- Font serif/sans được self-host và có đầy đủ glyph tiếng Việt, không phụ thuộc Google Fonts.
- Trang thống kê với biểu đồ Matplotlib cùng hệ màu giao diện.
- Responsive cho desktop, tablet và mobile; hỗ trợ `prefers-reduced-motion`.

> Có thể đặt biến môi trường `GUESTBOOK_SECRET` trước khi deploy để thay khóa session mặc định dành cho môi trường local.
