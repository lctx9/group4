import os
from openai import OpenAI

# 1. Tự động nạp cấu hình từ file .env bảo mật nếu có
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

print("--- KHỞI ĐỘNG KIỂM TRA API GATE E3 (CẬP NHẬT THEO PROPOSAL §5.3) ---")

# 2. Test kết nối đến Exploration Agent: Qwen3.6-Coder-35B-A3B-Instruct
qwen_key = os.getenv("QWEN_API_KEY")
qwen_base = os.getenv("QWEN_API_BASE", "https://dashscope.aliyuncs.com/compatible-mode/v1") # Hoặc base URL Ollama: http://localhost:11434/v1
qwen_model = os.getenv("QWEN_MODEL_NAME", "qwen3.6-coder-35b-instruct") # Hoặc tên model trên Ollama

if qwen_key:
    try:
        print(f"🤖 Đang kiểm tra Exploration Agent (Qwen) tại: {qwen_base}...")
        qwen_client = OpenAI(api_key=qwen_key, base_url=qwen_base)
        qwen_response = qwen_client.chat.completions.create(
            model=qwen_model,
            messages=[{"role": "user", "content": "Ping"}],
            max_tokens=5
        )
        print(f"✅ Qwen ({qwen_model}): KẾT NỐI THÀNH CÔNG! Phản hồi: {qwen_response.choices[0].message.content.strip()}")
    except Exception as e:
        print(f"❌ Qwen Lỗi: {e}")
else:
    print(f"⚠️ Qwen: Chưa cấu hình QWEN_API_KEY. Sẽ dùng chế độ giả lập (Mock Mode) khi chạy thực nghiệm.")

# 3. Test kết nối đến Code Action Fixer: DeepSeek V4 Pro
deepseek_key = os.getenv("DEEPSEEK_API_KEY")
deepseek_base = os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com/v1")
deepseek_model = os.getenv("DEEPSEEK_MODEL_NAME", "deepseek-reasoner") # deepseek-reasoner hỗ trợ thinking mode

if deepseek_key:
    try:
        print(f"🤖 Đang kiểm tra Code Action Fixer (DeepSeek) tại: {deepseek_base}...")
        deepseek_client = OpenAI(api_key=deepseek_key, base_url=deepseek_base)
        deepseek_response = deepseek_client.chat.completions.create(
            model=deepseek_model,
            messages=[{"role": "user", "content": "Ping"}],
            max_tokens=5
        )
        print(f"✅ DeepSeek ({deepseek_model}): KẾT NỐI THÀNH CÔNG! Phản hồi: {deepseek_response.choices[0].message.content.strip()}")
    except Exception as e:
        print(f"❌ DeepSeek Lỗi: {e}")
else:
    print(f"⚠️ DeepSeek: Chưa cấu hình DEEPSEEK_API_KEY. Sẽ dùng chế độ giả lập (Mock Mode) khi chạy thực nghiệm.")