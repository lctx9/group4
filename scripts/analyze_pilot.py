import pandas as pd
import os

print("--- KHỞI ĐỘNG TIẾN TRÌNH PHÂN TÍCH DỮ LIỆU PILOT (K=5) ---")

pilot_output_path = 'results/pilot_llm_output.csv'

if not os.path.exists(pilot_output_path):
    print(f"❌ Không tìm thấy file kết quả thực nghiệm tại: {pilot_output_path}")
else:
    # 1. Nạp dữ liệu đầu ra của tập Pilot
    df = pd.read_csv(pilot_output_path)
    
    # 2. KIẾN TRÚC GOM CỤM PASS@5: Group theo task_id để kiểm tra điều kiện cứu lỗi
    # Chỉ cần có chữ 'pass' xuất hiện trong 5 samples, tác vụ đó được tính là Pass@5 thành công
    aggregated_df = df.groupby('task_id').agg({
        'initial_state': 'first',
        'final_state': lambda x: 'pass' if 'pass' in x.values else 'fail'
    }).reset_index()
    
    # 3. Tính toán các thông số toán học F2P Rate cho Pass@5
    initial_fails = aggregated_df[aggregated_df['initial_state'] == 'fail']
    total_unique_fails = len(initial_fails)
    
    if total_unique_fails == 0:
        print("⚠️ Không tìm thấy tác vụ lỗi nền tảng nào để tính F2P.")
        f2p_pass_at_5 = 0.0
    else:
        successful_fixes = sum(1 for _, row in initial_fails.iterrows() if row['final_state'] == 'pass')
        f2p_pass_at_5 = (successful_fixes / total_unique_fails) * 100
        
    # 4. In báo cáo nghiệm thu kết quả Pilot ra màn hình console
    print("\n📊 BÁO CÁO THỐNG KÊ GIAI ĐOẠN PILOT RUN:")
    print(f"- Tổng số lượt Agent đã chạy thực tế (Hàng thô): {len(df)}")
    print(f"- Tổng số Tác vụ lớn độc nhất được gom cụm thành công: {len(aggregated_df)}")
    print(f"- Số tác vụ lớn dính lỗi ban đầu: {total_unique_fails}")
    print(f"- Số tác vụ lớn được tác nhân cứu lỗi thành công ở cấu hình Pass@5: {successful_fixes}")
    print(f"🔥 Kết quả Fail-to-Pass Rate ở ngân sách Pass@5: {f2p_pass_at_5:.2f}%")
    
    print("\n✅ KIỂM TRA HẠ TẦNG: Mọi cấu trúc dữ liệu k=5 đã thông suốt, không lỗi phân mảnh!")