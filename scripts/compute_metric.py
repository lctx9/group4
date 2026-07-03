def calculate_f2p(paired_results):
    """
    Hàm tính Fail-to-Pass Rate (F2P %) chuẩn TestExplora cho Nhóm 4.
    Đầu vào: Danh sách các cặp trạng thái dạng tuple (initial_state, final_state)
    - initial_state: Trạng thái kiểm thử hệ thống ban đầu ('fail' hoặc 'pass')
    - final_state: Trạng thái sau khi tác nhân thực hiện Exploration & Fix ('fail' hoặc 'pass')
    
    Công thức F2P chuẩn: (Số tác vụ chuyển từ Fail sang Pass) / (Tổng số tác vụ ban đầu bị Fail) * 100
    """
    # Lọc diện tác vụ ban đầu bị lỗi (Đúng bản chất cứu lỗi Proactive Discovery)
    initial_fails = [task for task in paired_results if task[0] == "fail"]
    total_initial_fails = len(initial_fails)
    
    if total_initial_fails == 0:
        print("⚠️ Không có tác vụ lỗi ban đầu nào để làm tập mẫu tính toán F2P.")
        return 0.0
    
    # Đếm số lượng tác vụ cứu lỗi thành công chuyển trạng thái từ Fail -> Pass
    saved_tasks = sum(1 for initial, final in initial_fails if final == "pass")
    
    f2p_rate = (saved_tasks / total_initial_fails) * 100
    return f2p_rate

print("--- KHỞI ĐỘNG KIỂM TRA METRIC SCRIPT GATE E4 ---")

# Giả lập bộ dữ liệu cặp trạng thái thực tế của 10 tác vụ (Mock data: (Trạng_thái_đầu, Trạng_thái_cuối))
mock_paired_results = [
    ("fail", "pass"),  # 1. Cứu thành công (Tính vào F2P)
    ("fail", "fail"),  # 2. Thất bại (Tính vào F2P)
    ("pass", "pass"),  # 3. Ban đầu tự pass -> Bỏ qua không tính vào mẫu F2P
    ("fail", "pass"),  # 4. Cứu thành công (Tính vào F2P)
    ("fail", "fail"),  # 5. Thất bại (Tính vào F2P)
    ("fail", "fail"),  # 6. Thất bại (Tính vào F2P)
    ("pass", "pass"),  # 7. Ban đầu tự pass -> Bỏ qua không tính vào mẫu F2P
    ("fail", "pass"),  # 8. Cứu thành công (Tính vào F2P)
    ("fail", "fail"),  # 9. Thất bại (Tính vào F2P)
    ("fail", "fail")   # 10. Thất bại (Tính vào F2P)
]

# Thực hiện tính toán
f2p = calculate_f2p(mock_paired_results)

# Trích xuất số liệu cấu trúc phục vụ in log
total_fails = sum(1 for initial, _ in mock_paired_results if initial == "fail")
successful_fixes = sum(1 for initial, final in mock_paired_results if initial == "fail" and final == "pass")

print(f"Tổng số mẫu giả lập đưa vào hệ thống (N): {len(mock_paired_results)}")
print(f"Số lượng tác vụ ban đầu dính lỗi (Mẫu tính F2P): {total_fails}")
print(f"Số lượng tác vụ tác nhân khôi phục thành công (Fail -> Pass): {successful_fixes}")
print(f"📊 Kết quả Fail-to-Pass Rate (F2P): {f2p:.2f}%")

# Kiểm tra tính chính xác của thuật toán (3 tác vụ cứu thành công / 8 mẫu lỗi = 37.5%)
if abs(f2p - 37.5) < 1e-5:
    print("✅ Gate E4: SCRIPT TÍNH METRIC CHẠY THÀNH CÔNG KHÔNG LỖI RUNTIME!")
else:
    print("❌ Gate E4: Thuật toán tính sai lệch công thức chuẩn của benchmark.")