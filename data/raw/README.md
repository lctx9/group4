# Metadata Dataset: TestExplora-Lite

- **Nguồn URL tải dữ liệu gốc:** github.com/microsoft/TestExplora
- **Bản quyền sở hữu (License):** MIT License (Microsoft Open Source)
- **Ngày tải dữ liệu về hệ thống:** 2026-06-20
- **Quy mô mẫu thực nghiệm (N):** 330 PRs, 517 mẫu đại diện đa ngành từ 482 repositories mã nguồn mở

## Định nghĩa cấu trúc các cột dữ liệu dữ thô
- `task_id`: Mã định danh băm duy nhất cho từng tác vụ kiểm thử cấp kho lưu trữ (repository-level).
- `repo`: Tên đường dẫn kho lưu trữ chứa mã nguồn gốc của bài toán cần quét lỗi logic.
- `base_commit`: Mã băm Git commit nền tảng tại thời điểm trước khi tiến hành sửa lỗi chức năng.
- `doc_context`: Đoạn văn bản đặc tả chức năng/hướng dẫn sử dụng được trích xuất để đối chiếu tìm lỗi.
- `test_suite_content`: Cấu trúc và nội dung chi tiết của bộ mã nguồn kiểm thử đi kèm.