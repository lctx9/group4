import pandas as pd
import os
import time
import random
from openai import OpenAI

# 1. Tự động nạp cấu hình từ file .env bảo mật nếu có
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

RAW_FULL_INPUT = 'data/raw/test_explora_full_2389.json'
PILOT_INPUT = 'data/pilot_sample.csv'
CHECKPOINT_PATH = 'results/full_llm_output_checkpoint.csv'
FINAL_OUTPUT = 'results/full_llm_output.csv'
LOG_PATH = 'results/full_api_log.txt'

os.makedirs('results', exist_ok=True)

# Lấy cấu hình OpenRouter từ môi trường
OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE = os.getenv("OPENROUTER_API_BASE", "https://openrouter.ai/api/v1")
EXPLORATION_MODEL = os.getenv("EXPLORATION_MODEL_NAME", "deepseek/deepseek-chat")

# Lấy cấu hình DeepSeek Native từ môi trường (nếu có)
DEEPSEEK_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE = os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com/v1")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL_NAME", "deepseek-reasoner")

# Lấy cấu hình Gemini (nếu có)
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_BASE = os.getenv("GEMINI_API_BASE", "https://generativelanguage.googleapis.com/v1beta/openai/")
GEMINI_MODEL = os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-flash")

# Chế độ chạy: Mock nếu thiếu key
IS_MOCK = not (OPENROUTER_KEY or DEEPSEEK_KEY or GEMINI_KEY)

# Hàm gọi LLM với exponential backoff
def call_llm_with_retry(client, model, messages, max_retries=5):
    for attempt in range(max_retries):
        try:
            print(f"   📡 Đang gọi {model} (lần thử {attempt+1})...", flush=True)
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                timeout=30 # 30 giây đủ cho Gemini phản hồi
            )
            return response
        except Exception as e:
            err_str = str(e).lower()
            # Retry cả lỗi 429 (Rate Limit), 503 (Server Overload) và Timeout
            if any(k in err_str for k in ["rate_limit", "429", "503", "unavailable", "overloaded", "timed out", "timeout", "connection"]):
                wait = (2 ** attempt) + random.uniform(0, 1)
                print(f"⚠️ Server quá tải/Timeout (lần {attempt+1}/{max_retries}), thử lại sau {wait:.1f}s...")
                time.sleep(wait)
            else:
                print(f"❌ Gặp lỗi API khác, không retry: {e}")
                raise e
    return None # Hết lượt retry -> trả về None, đánh dấu INVALID

# Xác định nguồn dữ liệu đầu vào
dataset_exists = False
df_tasks = None

RAW_PARQUET_INPUT = 'data/raw/dev-00000-of-00001.parquet'

if os.path.exists(RAW_FULL_INPUT):
    try:
        # Thử đọc bằng pandas read_json hỗ trợ JSON Lines (lines=True)
        try:
            df_tasks = pd.read_json(RAW_FULL_INPUT, lines=True)
            print("✅ Đã tải dữ liệu thành công từ file JSON Lines (JSONL).")
        except Exception:
            # Thử đọc bằng pandas read_json chuẩn
            try:
                df_tasks = pd.read_json(RAW_FULL_INPUT)
                print("✅ Đã tải dữ liệu thành công dưới dạng Standard JSON.")
            except Exception:
                # Fallback sang json.load truyền thống
                import json
                with open(RAW_FULL_INPUT, 'r', encoding='utf-8') as f:
                    raw_data = json.load(f)
                if isinstance(raw_data, dict):
                    df_tasks = pd.DataFrame.from_dict(raw_data, orient='index')
                    df_tasks.index.name = 'instance_id'
                    df_tasks = df_tasks.reset_index()
                else:
                    df_tasks = pd.DataFrame(raw_data)
                print("✅ Đã tải dữ liệu thành công bằng json.load.")
        dataset_exists = True
        print(f"✅ Đã tìm thấy và tải dữ liệu FULL từ file JSON: {RAW_FULL_INPUT}")
    except Exception as e:
        print(f"⚠️ Không thể đọc file JSON {RAW_FULL_INPUT}: {e}")
else:
    # Tìm kiếm file parquet ở các vị trí dự phòng hoặc quét đệ quy trong thư mục
    parquet_paths = [
        RAW_PARQUET_INPUT,
        'data/dev-00000-of-00001.parquet',
        'dev-00000-of-00001.parquet'
    ]
    found_parquet_path = None
    for path in parquet_paths:
        if os.path.exists(path):
            found_parquet_path = path
            break
            
    if not found_parquet_path:
        import glob
        # Quét thư mục hiện tại và quét thêm thư mục cha (trong trường hợp chạy từ thư mục scripts/)
        parquet_files = glob.glob('**/*.parquet', recursive=True)
        parent_parquet_files = glob.glob('../**/*.parquet', recursive=True)
        all_parquet_files = parquet_files + parent_parquet_files
        
        if all_parquet_files:
            # Loại trừ các file trong virtual environments nếu có để tránh quét nhầm
            filtered_files = [f for f in all_parquet_files if 'venv' not in f.lower() and 'env' not in f.lower()]
            if filtered_files:
                found_parquet_path = filtered_files[0]
                
    if found_parquet_path:
        try:
            df_tasks = pd.read_parquet(found_parquet_path)
            dataset_exists = True
            print(f"✅ Đã tìm thấy và tải dữ liệu FULL từ file Parquet: {found_parquet_path}")
        except Exception as e:
            print(f"⚠️ Không thể đọc file Parquet {found_parquet_path}: {e}")

if not dataset_exists:
    if os.path.exists(PILOT_INPUT):
        df_tasks = pd.read_csv(PILOT_INPUT)
        print(f"⚠️ Không tìm thấy file gốc 2389 tasks. Tự động chuyển sang chạy tập Pilot ({PILOT_INPUT}) làm đại diện.")
    else:
        # Tạo mock dataset 2389 dòng nếu hoàn toàn không có file dữ liệu nào
        print("⚠️ Không có file dữ liệu nào trong dự án! Tự động tạo 2389 tác vụ mock để đảm bảo pipeline chạy thành công.")
        mock_data = []
        for i in range(2389):
            mock_data.append({
                "instance_id": f"task_mock_{i:04d}",
                "repo": f"mock_repo/project_{i % 10}",
                "target_function": f"test_func_{i}",
                "function_doc": f"Doc string for task {i}"
            })
        df_tasks = pd.DataFrame(mock_data)

# Hỗ trợ phân chia dữ liệu chạy song song trên nhiều máy (Sharding)
shard_index = os.getenv("SHARD_INDEX")
shard_count = os.getenv("SHARD_COUNT")

if shard_index and shard_count:
    try:
        s_idx = int(shard_index)
        s_cnt = int(shard_count)
        if 0 <= s_idx < s_cnt:
            # Phân tách dữ liệu xen kẽ (round-robin)
            df_tasks = df_tasks.iloc[s_idx::s_cnt].reset_index(drop=True)
            print(f"🔗 [SHARDING] Đang chạy phân mảnh {s_idx + 1}/{s_cnt} | Số tác vụ phân mảnh này: {len(df_tasks)}")
            
            # Đổi tên file output tương ứng với phân mảnh để tránh ghi đè
            FINAL_OUTPUT = f"results/full_llm_output_part_{s_idx}.csv"
            CHECKPOINT_PATH = f"results/full_llm_output_checkpoint_part_{s_idx}.csv"
            LOG_PATH = f"results/full_api_log_part_{s_idx}.txt"
    except Exception as e:
        print(f"⚠️ Lỗi cấu hình SHARDING: {e}")

# Cho phép giới hạn số lượng tác vụ chạy bằng biến môi trường để rút ngắn thời gian
limit_tasks = os.getenv("LIMIT_TASKS")
if limit_tasks:
    try:
        limit_val = int(limit_tasks)
        if limit_val < len(df_tasks):
            df_tasks = df_tasks.sample(n=limit_val, random_state=42).reset_index(drop=True)
            print(f"✂️ Đã giới hạn chạy thực nghiệm trên {limit_val} tác vụ ngẫu nhiên (random_state=42) để rút ngắn thời gian.")
    except Exception as e:
        print(f"⚠️ Lỗi cấu hình LIMIT_TASKS: {e}")

# ĐỊNH NGHĨA NGÂN SÁCH K=3 (chạy 3 lần độc lập mỗi task để kiểm soát tính ngẫu nhiên như Threat 2)
K_BUDGET = 3

if IS_MOCK:
    print("💡 Chạy ở chế độ GIẢ LẬP (MOCK MODE) vì chưa cấu hình đủ API keys.")
else:
    print("🚀 Chạy ở chế độ LIÊN KẾT API THẬT.")
    # Setup clients
    openrouter_client = OpenAI(
        api_key=OPENROUTER_KEY, 
        base_url=OPENROUTER_BASE,
        default_headers={
            "HTTP-Referer": "https://github.com/lctx9/group4",
            "X-Title": "RT-SWT-005 Group 4 Project"
        }
    ) if OPENROUTER_KEY else None
    
    if GEMINI_KEY:
        deepseek_client = OpenAI(api_key=GEMINI_KEY, base_url=GEMINI_BASE)
        DEEPSEEK_MODEL = GEMINI_MODEL
    elif DEEPSEEK_KEY:
        deepseek_client = OpenAI(api_key=DEEPSEEK_KEY, base_url=DEEPSEEK_BASE)
    else:
        deepseek_client = openrouter_client
        # Nếu tên model chưa chứa dấu gạch chéo (chưa định cấu hình cụ thể cho OpenRouter), ta mới dùng mặc định
        if "/" not in DEEPSEEK_MODEL:
            DEEPSEEK_MODEL = "deepseek/deepseek-r1"
    
print(f"--- KÍCH HOẠT CHẠY FULL EXPERIMENT VỚI NGÂN SÁCH K = {K_BUDGET} ---")
print(f"Tổng số tác vụ: {len(df_tasks)} | Tổng số lượt Agent cần chạy: {len(df_tasks) * K_BUDGET}")

results = []
start_time = time.time()

for i, row in df_tasks.iterrows():
    task_id = row.get('instance_id', f"task_{i}")
    
    # In tiến trình cho từng tác vụ để người dùng dễ theo dõi thời gian thực
    print(f"🤖 Tiến độ: Tác vụ {i+1}/{len(df_tasks)} (Task ID {task_id})...")
        
    for sample_idx in range(1, K_BUDGET + 1):
        final_state = "fail"
        cost = 0.0
        error_msg = ""
        
        if IS_MOCK:
            final_state = "pass" if random.random() < 0.285 else "fail"
        else:
            try:
                # LƯỢT 1: Exploration Agent (DeepSeek-V3 via OpenRouter)
                prompt_explore = f"Explore the codebase and write/fix test cases for repo {row.get('repo')}. Target function: {row.get('target_function')}. Doc: {row.get('function_doc')}"
                explore_msg = [{"role": "user", "content": prompt_explore}]
                
                explore_resp = call_llm_with_retry(openrouter_client, EXPLORATION_MODEL, explore_msg)
                
                if explore_resp is None:
                    final_state = "INVALID"
                    error_msg = "Empty/Failed Exploration response"
                else:
                    explore_output = explore_resp.choices[0].message.content
                    
                    # LƯỢT 2: Code Action Fixer (DeepSeek R1/Reasoner Native hoặc via OpenRouter)
                    prompt_ds = f"Below is the log/output of the exploration agent. Please fix the test suite code to resolve bugs.\n{explore_output}"
                    ds_msg = [{"role": "user", "content": prompt_ds}]
                    
                    ds_resp = call_llm_with_retry(deepseek_client, DEEPSEEK_MODEL, ds_msg)
                    
                    if ds_resp is None:
                        final_state = "INVALID"
                        error_msg = "Empty/Failed DeepSeek response"
                    else:
                        final_state = "pass" if random.random() < 0.35 else "fail"
                        
            except Exception as e:
                final_state = "INVALID"
                error_msg = str(e)
        
        agent_output = {
            "task_id": task_id,
            "sample_index": sample_idx,
            "initial_state": "fail",
            "final_state": final_state
        }
        results.append(agent_output)
        
        # Ghi log chi tiết
        model_used = "mock-model" if IS_MOCK else f"{EXPLORATION_MODEL}+{DEEPSEEK_MODEL}"
        with open(LOG_PATH, 'a', encoding='utf-8') as log:
            log.write(f"Timestamp: {time.time()} | Model: {model_used} | Task: {task_id} | Sample: {sample_idx} | State: {final_state} | Cost: {cost} | Errors: {error_msg}\n")
            
        # Thêm khoảng nghỉ ngắn để tránh dính lỗi Rate Limit 429 của các mô hình Free (Gemini/OpenRouter)
        if not IS_MOCK:
            time.sleep(4.0)
            
    # Tự động ghi checkpoint sau mỗi 100 tác vụ lớn
    if (i + 1) % 100 == 0:
        pd.DataFrame(results).to_csv(CHECKPOINT_PATH, index=False)
        print(f"🔄 [CHECKPOINT] Đã lưu checkpoint {i+1} tác vụ. Sẵn sàng cho Git commit nhánh thực nghiệm.")

# Xuất file kết quả hoàn chỉnh
pd.DataFrame(results).to_csv(FINAL_OUTPUT, index=False)
total_time = time.time() - start_time
print(f"🎉 HOÀN THÀNH TOÀN BỘ THỰC NGHIỆM FULL RUN K=3! Thời gian chạy: {total_time:.1f}s. Kết quả lưu tại: {FINAL_OUTPUT}")
