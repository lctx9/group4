import pandas as pd
import json
import os

print("--- TIẾN HÀNH TRÍCH XUẤT TẬP PILOT THEO ĐỊNH DANH ĐỘC NHẤT ---")

raw_file_path = 'data/raw/test_explora_full_2389.json' 
output_pilot_path = 'data/pilot_sample.csv'

if not os.path.exists(raw_file_path):
    print(f"❌ Không tìm thấy file gốc tại: {raw_file_path}")
else:
    # 1. Đọc file JSON gốc
    with open(raw_file_path, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
        
    if isinstance(raw_data, dict):
        raw_df = pd.DataFrame.from_dict(raw_data, orient='index')
        raw_df.index.name = 'task_id'
        raw_df = raw_df.reset_index()
    else:
        raw_df = pd.DataFrame(raw_data)
        
    print("\n🔍 LOG PHÂN TÍCH CẤU TRÚC DATASET:")
    print(f"- Tổng số dòng thô phát hiện trong file: {len(raw_df)}")
    print(f"- Các cột hiện có trong file: {list(raw_df.columns)}")
    
    # 2. Tự động nhận diện cột chứa mã định danh tác vụ (ID)
    id_col = None
    for col in ['instance_id', 'task_id', 'id', 'index', raw_df.columns[0]]:
        if col in raw_df.columns:
            id_col = col
            break
            
    # Lấy ra danh sách các ID độc nhất
    unique_ids = raw_df[id_col].unique()
    print(f"- Đã chọn cột định danh chính: '{id_col}'")
    print(f"- Tổng số Tác vụ lớn độc nhất (Unique Tasks): {len(unique_ids)}")
    
    # 3. Lấy mẫu 10% dựa trên ID độc nhất (Nếu có ~2389 ID, máy sẽ bốc ~239 ID)
    sampled_ids = pd.Series(unique_ids).sample(frac=0.10, random_state=42).values
    
    # 4. Lọc toàn bộ các dòng thuộc về 10% ID đã chọn
    pilot_df = raw_df[raw_df[id_col].isin(sampled_ids)]
    
    # 5. Lưu kết quả
    os.makedirs(os.path.dirname(output_pilot_path), exist_ok=True)
    pilot_df.to_csv(output_pilot_path, index=False)
    
    print(f"\n✅ ĐÃ FIX VÀ TRIỂN KHAI THÀNH CÔNG:")
    print(f"- Đã chọn ngẫu nhiên: {len(sampled_ids)} Tác vụ lớn độc nhất (Đúng chuẩn 10% tập tổng).")
    print(f"- Tổng số dòng dữ liệu con tương ứng được gom vào tập Pilot: {len(pilot_df)} dòng.")
    print(f"💾 File mẫu Pilot chuẩn khoa học đã lưu tại: {output_pilot_path}")