import pandas as pd
import glob
import os

print("--- KHỞI ĐỘNG GỘP CÁC PHÂN MẢNH KẾT QUẢ THỰC NGHIỆM ---")

# Tìm toàn bộ các file phân mảnh có đuôi csv trong thư mục results
raw_files = glob.glob('results/full_llm_output_part*.csv')
# Loại bỏ file kết quả tổng hợp chính nếu trùng tên
files = [f for f in raw_files if os.path.basename(f) != 'full_llm_output.csv']

if not files:
    print("❌ Không tìm thấy phân mảnh kết quả nào có dạng: results/full_llm_output_part*.csv")
else:
    print(f"🔍 Tìm thấy {len(files)} phân mảnh kết quả: {files}")
    dfs = []
    
    for f in files:
        try:
            df_part = pd.read_csv(f)
            dfs.append(df_part)
            print(f"✅ Đã nạp thành công: {f} ({len(df_part)} dòng)")
        except Exception as e:
            print(f"❌ Lỗi khi đọc tệp {f}: {e}")
            
    if dfs:
        # Gộp tất cả các DataFrame lại thành một
        df_all = pd.concat(dfs, ignore_index=True)
        
        # Sắp xếp lại cho đẹp mắt theo task_id và sample_index
        if 'task_id' in df_all.columns and 'sample_index' in df_all.columns:
            df_all = df_all.sort_values(by=['task_id', 'sample_index']).reset_index(drop=True)
            
        output_file = 'results/full_llm_output.csv'
        df_all.to_csv(output_file, index=False)
        print(f"\n🎉 GỘP PHÂN MẢNH THÀNH CÔNG!")
        print(f"💾 File tổng hợp hoàn chỉnh ({len(df_all)} dòng) đã được lưu tại: {output_file}")
        print("💡 Bây giờ bạn có thể tiến hành chạy phân tích thống kê (analyze_full_experiment.py) bình thường.")
