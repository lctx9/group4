import numpy as np

def calculate_f2p(test_results):
    """
    Hàm tính Fail-to-Pass Rate (F2P %) chuẩn RBL-4 của Nhóm 4.
    Đầu vào: Danh sách trạng thái kết quả test suite sau khi Agent xử lý:
    - 'pass': Agent đã cứu và sửa test suite thành công từ trạng thái lỗi.
    - 'fail': Agent thất bại, test suite vẫn dính lỗi.
    """
    total_tasks = len(test_results)
    if total_tasks == 0:
        return 0.0
    
    # Đếm số lượng task ban đầu bị lỗi (Fail) nhưng Agentic Exploration đã cứu thành công (Pass)
    saved_tasks = sum(1 for result in test_results if result == "pass")
    
    f2p_rate = (saved_tasks / total_tasks) * 100
    return f2p_rate

print("--- KHỞI ĐỘNG KIỂM TRA METRIC SCRIPT GATE E4 ---")

# Giả lập dữ liệu kết quả đầu ra của 10 tasks (Mock data)
# Giả sử Agent sửa thành công 3 tasks ("pass"), còn 7 tasks vẫn chịu chết ("fail")
mock_results = ["pass", "fail", "fail", "pass", "fail", "fail", "fail", "pass", "fail", "fail"]

f2p = calculate_f2p(mock_results)

print(f"Tổng số mẫu giả lập chạy thử (N): {len(mock_results)}")
print(f"Số lượng task Agent sửa thành công: {mock_results.count('pass')}")
print(f"📊 Kết quả Fail-to-Pass Rate (F2P): {f2p:.2f}%")

# Kiểm tra logic tính toán để tự động xác nhận Pass Gate E4
if f2p == 30.0:
    print("✅ Gate E4: SCRIPT TÍNH METRIC CHẠY THÀNH CÔNG KHÔNG LỖI RUNTIME!")
else:
    print("❌ Gate E4: Tính toán sai lệch công thức.")