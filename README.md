# Sổ lưu bút (Guestbook)

Ứng dụng web sổ lưu bút viết bằng Python và Django thuần với kiến trúc Server-Side Rendering (SSR), không sử dụng frontend rời.

## Chức năng

- **Trang chủ (`/`)**: Hiển thị danh sách tất cả lời nhắn đã lưu trong cơ sở dữ liệu.
- **Viết lời nhắn (`/add`)**: Form nhập tên và nội dung lời nhắn; xác thực dữ liệu hợp lệ và lưu trữ.
- **Xóa lời nhắn (`/delete/<int:id>`)**: Xóa lời nhắn theo ID và chuyển hướng về trang chủ (tự động dồn lại số thứ tự ID).
- **Thống kê (`/stats`)**:
  - Tổng số lời nhắn đã ghi.
  - Tổng số người gửi.
  - Danh sách top 5 người gửi nhiều lời nhắn nhất.
  - Biểu đồ cột minh họa số lượng lời nhắn theo từng người gửi (sinh bằng Matplotlib chất lượng cao, lưu file ảnh `static/stats.png`).
- **Lưu trữ đồng bộ JSON (`data/data.json`)**: Tự động nạp dữ liệu khi khởi chạy ứng dụng và đồng bộ hóa file JSON mỗi khi thêm hoặc xóa lời nhắn.
- **Tài liệu API Swagger (`/api/docs/`)**: Hỗ trợ Swagger UI và ReDoc xem tài liệu API.

## Hướng dẫn cài đặt và chạy sau khi clone

### 1. Clone dự án

```bash
git clone https://github.com/zzei5126/Python-web-project.git
cd Python-web-project
```

### 2. Tạo và kích hoạt môi trường ảo

- **Windows (PowerShell)**:
  ```powershell
  python -m venv .venv
  .venv\Scripts\Activate.ps1
  ```

- **Windows (CMD)**:
  ```cmd
  python -m venv .venv
  .venv\Scripts\activate.bat
  ```

- **macOS / Linux**:
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 3. Cài đặt các thư viện cần thiết

```bash
pip install -r backend/requirements.txt
```

### 4. Tạo file cấu hình môi trường (.env)

- **Windows (PowerShell)**:
  ```powershell
  Copy-Item backend/.env.example backend/.env
  ```

- **Windows (CMD)**:
  ```cmd
  copy backend\.env.example backend\.env
  ```

- **macOS / Linux**:
  ```bash
  cp backend/.env.example backend/.env
  ```

### 5. Khởi tạo cơ sở dữ liệu và thu thập file tĩnh

```bash
cd backend
python manage.py migrate
python manage.py collectstatic --noinput
```

### 6. Khởi chạy máy chủ phát triển

```bash
python manage.py runserver
```

Mở trình duyệt và truy cập:
- **Trang web chính**: `http://127.0.0.1:8000/`
- **Tài liệu Swagger UI**: `http://127.0.0.1:8000/api/docs/`
