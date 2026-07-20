import pandas as pd
import glob
import os

print("--- KHỞI ĐỘNG GỘP CÁC PHÂN MẢNH KẾT QUẢ THỰC NGHIỆM ---")

# Tìm toàn bộ các file phân mảnh (ưu tiên index*.csv của đợt chạy K=3)
raw_index_files = glob.glob('results/index*.csv')
ignored_filenames = {'full_llm_output.csv', 'pilot_llm_output.csv', 'pilot_llm_output_checkpoint.csv', 'summary.csv', 'full_llm_output_checkpoint.csv'}

files = [f for f in raw_index_files if os.path.basename(f) not in ignored_filenames]

if not files:
    # Fallback sang full_llm_output_part*.csv nếu không có index*.csv
    raw_part_files = glob.glob('results/full_llm_output_part*.csv')
    files = [f for f in raw_part_files if os.path.basename(f) not in ignored_filenames]

if not files:
    print("❌ Không tìm thấy phân mảnh kết quả nào có dạng: results/index*.csv hoặc results/full_llm_output_part*.csv")
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
