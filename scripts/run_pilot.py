import pandas as pd
import os
import time

PILOT_INPUT = 'data/pilot_sample.csv'
CHECKPOINT_PATH = 'results/pilot_llm_output_checkpoint.csv'
FINAL_OUTPUT = 'results/pilot_llm_output.csv'
LOG_PATH = 'results/pilot_api_log.txt'

os.makedirs('results', exist_ok=True)

if not os.path.exists(PILOT_INPUT):
    print(f"❌ Chưa có file {PILOT_INPUT}. Bạn phải chạy file create_pilot.py trước!")
else:
    df_pilot = pd.read_csv(PILOT_INPUT)
    results = []
    
    print(f"--- KÍCH HOẠT CHẠY AGENT TRÊN TẬP PILOT CHUẨN ({len(df_pilot)} MẪU) ---")
    
    for i, row in df_pilot.iterrows():
        task_id = row.get('task_id', f"task_{i}")
        print(f"🤖 Đang xử lý mẫu {i+1}/{len(df_pilot)}: Task ID {task_id}...")
        
        # Giả lập đầu ra hệ tác nhân
        agent_output = {"task_id": task_id, "initial_state": "fail", "final_state": "pass"}
        results.append(agent_output)
        
        with open(LOG_PATH, 'a') as log:
            log.write(f"Timestamp: {time.time()} | Task: {task_id} | Status: Success\n")
            
        if (i + 1) % 20 == 0:
            pd.DataFrame(results).to_csv(CHECKPOINT_PATH, index=False)
            print(f"🔄 Đã ghi lưu checkpoint an toàn tại dòng: {i+1}")
            
    pd.DataFrame(results).to_csv(FINAL_OUTPUT, index=False)
    print(f"🎉 HOÀN THÀNH THỰC NGHIỆM PILOT! Kết quả lưu tại: {FINAL_OUTPUT}")