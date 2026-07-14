# Danh Sách Các Công Việc Cần Thực Hiện - Tuần 8 (Full Experiment)

Tệp này ghi nhận các bước bạn và nhóm cần thực hiện tiếp theo để hoàn thành thực nghiệm Tuần 8, tính toán số liệu và vẽ biểu đồ cho báo cáo cuối kỳ.

## 📋 Hướng Dẫn Từng Bước

### Bước 1: Kiểm Tra Toàn Bộ Luồng Code (Chạy thử Mock)
- [ ] Chạy thử lệnh chạy Pilot ở chế độ Mock để xác nhận không lỗi cú pháp:
  ```bash
  python scripts/run_pilot.py
  ```
- [ ] Kiểm tra kết quả phân tích dữ liệu Pilot (đảm bảo F2P tính ở cấu hình k=1):
  ```bash
  python scripts/analyze_pilot.py
  ```
- [ ] Chạy thử nghiệm Full Run ở chế độ Mock để tạo dữ liệu giả lập (2389 dòng x K=3):
  ```bash
  python scripts/run_full_experiment.py
  ```
- [ ] Chạy thử phân tích thống kê Wilcoxon & Cliff's delta trên dữ liệu giả lập:
  ```bash
  python scripts/analyze_full_experiment.py
  ```
- [ ] Vẽ biểu đồ kết quả (300 DPI) vào thư mục `figures/`:
  ```bash
  python scripts/generate_figures.py
  ```

---

### Bước 2: Commit và Lưu Trữ Code (Gate E7)
- [ ] Commit toàn bộ các script đã sửa đổi và tạo mới lên Git:
  ```bash
  git add scripts/ results/ full_analysis.ipynb
  git commit -m "feat: align experimental pipeline with proposal (k=1 budget, Wilcoxon, Cliff's delta, 300 DPI figures)"
  ```
- [ ] Push code lên GitHub để tránh mất dữ liệu:
  ```bash
  git push origin main  # Hoặc tên nhánh của nhóm
  ```

---

### Bước 3: Chạy Thực Nghiệm Thật Trên Cloud (Google Colab / Kaggle)
- [ ] Chuẩn bị các API key của nhóm (`QWEN_API_KEY` và `DEEPSEEK_API_KEY`).
- [ ] Mở Google Colab / Kaggle và upload thư mục dự án lên, hoặc clone từ repo GitHub về notebook.
- [ ] Cấu hình biến môi trường chứa API key trong notebook hoặc file `.env`:
  ```python
  import os
  os.environ["QWEN_API_KEY"] = "Nhập_Key_Qwen_Ở_Đây"
  os.environ["DEEPSEEK_API_KEY"] = "Nhập_Key_DeepSeek_Ở_Đây"
  ```
- [ ] Chạy thực nghiệm thật trên toàn bộ dataset (chạy file `run_full_experiment.py` từ notebook):
  ```bash
  !python scripts/run_full_experiment.py
  ```
  *(Quá trình này sẽ gọi API thật, tự động áp dụng exponential backoff khi gặp lỗi rate limit 429 và ghi log chi tiết)*.

---

### Bước 4: Phân Tích Thống Kê & Vẽ Biểu Đồ Thực Tế
- [ ] Mở file [results/full_analysis.ipynb](results/full_analysis.ipynb) trên môi trường chạy thực tế và thực thi cell phân tích thống kê.
- [ ] Kiểm tra kết quả trong file `results/summary.csv` để lấy các giá trị:
  - Average F2P Rate (%) của Agentic
  - p-value của kiểm định Wilcoxon
  - Cliff's delta (Effect Size)
  - Số lượng mẫu quan sát (N)
- [ ] Chạy file `generate_figures.py` để xuất 2 biểu đồ so sánh và phân phối thực tế.
- [ ] Tải 2 biểu đồ PNG từ thư mục `figures/` về máy tính để chuẩn bị đưa vào báo cáo.

---

### Bước 5: Kết Luận Giả Thuyết (Viết Báo Cáo)
- [ ] Đọc kết quả trong `results/summary.csv`.
- [ ] Xác nhận xem có bác bỏ được giả thuyết không ($H_0$) (nếu `p-value` < 0.05 và Average F2P > 16.06%):
  - **Reject H0:** Kết luận phương pháp tác nhân tự trị Agentic Exploration vượt trội hơn Plain baseline ở mức ý nghĩa 5%.
  - **Fail to reject H0:** Kết luận chưa đủ cơ sở chứng minh Agentic tốt hơn Plain baseline.
