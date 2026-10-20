# Sổ lưu bút (Guestbook) — Django SSR

Ứng dụng web sổ lưu bút viết bằng Python và Django thuần với kiến trúc Server-Side Rendering (SSR), không sử dụng frontend rời.

## Chức năng

- **Trang chủ (`/`)**: Hiển thị danh sách tất cả lời nhắn đã lưu trong cơ sở dữ liệu.
- **Viết lời nhắn (`/add`)**: Form nhập tên và nội dung lời nhắn; xác thực dữ liệu hợp lệ và lưu trữ.
- **Xóa lời nhắn (`/delete/<int:id>`)**: Xóa lời nhắn theo ID và chuyển hướng về trang chủ.
- **Thống kê (`/stats`)**:
  - Tổng số lời nhắn đã ghi.
  - Tổng số người gửi.
  - Danh sách top 5 người gửi nhiều lời nhắn nhất.
  - Biểu đồ cột minh họa số lượng lời nhắn theo từng người gửi (sinh bằng Matplotlib, lưu file ảnh `static/stats.png`).
- **Lưu trữ đồng bộ JSON (`data/data.json`)**: Tự động tải dữ liệu khi khởi chạy ứng dụng và đồng bộ hóa file JSON mỗi khi thêm hoặc xóa lời nhắn.

## Cài đặt và chạy

1. Kích hoạt môi trường ảo:

```powershell
.venv\Scripts\Activate.ps1
```

2. Cài đặt thư viện:

```bash
pip install -r backend/requirements.txt
```

3. Khởi động ứng dụng:

```bash
python backend/start.py
```

Truy cập trình duyệt tại: `http://127.0.0.1:8000`
