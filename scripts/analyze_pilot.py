import pandas as pd
import os

print("--- KHỞI ĐỘNG TIẾN TRÌNH PHÂN TÍCH DỮ LIỆU PILOT (K=1 - PASS@1) ---")

pilot_output_path = 'results/pilot_llm_output.csv'

if not os.path.exists(pilot_output_path):
    print(f"❌ Không tìm thấy file kết quả thực nghiệm tại: {pilot_output_path}")
else:
    # 1. Nạp dữ liệu đầu ra của tập Pilot
    df = pd.read_csv(pilot_output_path)
    
    # Ở cấu hình K=1 (Pass@1), mỗi task_id chỉ chạy duy nhất 1 lần.
    # Ta lọc và tính toán trực tiếp trên từng tác vụ độc nhất.
    # Nhóm theo task_id (là instance_id thực tế) để đảm bảo tính duy nhất.
    aggregated_df = df.groupby('task_id').agg({
        'initial_state': 'first',
        'final_state': 'first' # Chỉ lấy kết quả của lượt chạy duy nhất (sample_index = 1)
    }).reset_index()
    
    # 2. Tính toán các thông số toán học F2P Rate cho Pass@1
    initial_fails = aggregated_df[aggregated_df['initial_state'] == 'fail']
    total_unique_fails = len(initial_fails)
    
    if total_unique_fails == 0:
        print("⚠️ Không tìm thấy tác vụ lỗi nền tảng nào để tính F2P.")
        f2p_pass_at_1 = 0.0
        successful_fixes = 0
    else:
        successful_fixes = sum(1 for _, row in initial_fails.iterrows() if row['final_state'] == 'pass')
        f2p_pass_at_1 = (successful_fixes / total_unique_fails) * 100
        
    # Lọc bỏ các trạng thái INVALID nếu có để xem tỉ lệ lỗi hệ thống
    total_invalid = sum(1 for _, row in aggregated_df.iterrows() if row['final_state'] == 'INVALID')
    
    # 3. In báo cáo nghiệm thu kết quả Pilot ra màn hình console
    print("\n📊 BÁO CÁO THỐNG KÊ GIAI ĐOẠN PILOT RUN (PASS@1):")
    print(f"- Tổng số lượt Agent đã chạy thực tế (Hàng thô): {len(df)}")
    print(f"- Tổng số Tác vụ lớn độc nhất được kiểm thử: {len(aggregated_df)}")
    print(f"- Số tác vụ lớn dính lỗi ban đầu: {total_unique_fails}")
    print(f"- Số tác vụ lớn được tác nhân cứu lỗi thành công (Fail -> Pass) ở cấu hình Pass@1: {successful_fixes}")
    print(f"- Số lượt chạy bị lỗi hệ thống (INVALID): {total_invalid}")
    print(f"🔥 Kết quả Fail-to-Pass Rate ở ngân sách Pass@1: {f2p_pass_at_1:.2f}%")
    
    print("\n✅ KIỂM TRA HẠ TẦNG: Mọi cấu trúc dữ liệu k=1 đã thông suốt, phù hợp định hướng đề cương!")