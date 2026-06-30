## Nhật ký thực nghiệm - Nhóm 4 (Cập nhật ngày 30/06/2026)

### 1. Trạng thái 7 Cổng Kiểm Soát (Gate Checklist)
- [x] **E1 (Proposal duyệt):** Đã được duyệt.
- [x] **E2 (Dataset):** Đã tải dataset gốc lưu tại local máy chạy thực nghiệm.
- [x] **E3 (API test):** Code `test_api.py` đã thông suốt cấu trúc gọi đến OpenAI và Anthropic.
- [x] **E4 (Metric script):** Đã chạy thử `compute_metric.py` giả lập tính F2P đạt kết quả 30.00% không lỗi runtime.
- [x] **E5 (Ground truth plan):** Xác nhận hệ thống sử dụng bộ phán quyết tự động DocAgent (Automated Oracle) tích hợp sẵn trong framework TestExplora của Microsoft để kiểm tra ngữ nghĩa (Documentation-derived intent). Quy trình gán nhãn hoàn toàn tự động, không áp dụng chấm tay thủ công (IAA = N/A).
- [x] **E6 (Budget):** Đã tái tính toán ngân sách dự kiến cho >1,000 mẫu (~$160). Sẵn sàng kích hoạt phương án dự phòng chuyển đổi sang DeepSeek/Qwen nếu Pilot vượt ngân sách.
- [x] **E7 (GitHub Clean):** Đã cấu hình và push file `.gitignore` sạch lên nhánh main.

### 2. Thông số thiết lập ngẫu nhiên cho Tuần 7 (Pilot Setup)
- **Random Seed chọn mẫu Pilot:** 42
- **Tỷ lệ trích mẫu:** 10% tổng dữ liệu thô.