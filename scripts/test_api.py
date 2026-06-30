import os
from openai import OpenAI
from anthropic import Anthropic

# 1. Tự động nạp cấu hình từ file .env bảo mật
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

print("--- KHỞI ĐỘNG KIỂM TRA API GATE E3 ---")

# 2. Test kết nối đến OpenAI (GPT-5-mini)
openai_key = os.getenv("OPENAI_API_KEY")
if openai_key:
    try:
        openai_client = OpenAI(api_key=openai_key)
       # Gọi thử một request siêu nhẹ để check kết nối và số dư tài khoản
        openai_response = openai_client.chat.completions.create(
            model="gpt-5-mini", # Bám sát model trong proposal §5.3
            messages=[{"role": "user", "content": "Ping"}],
            max_completion_tokens=5  # <--- ĐÃ SỬA TÊN THAM SỐ TẠI ĐÂY CHÈN THAY MAX_TOKENS
        )
        print("✅ OpenAI (gpt-5-mini): KẾT NỐI THÀNH CÔNG!")
    except Exception as e:
        print(f"❌ OpenAI Lỗi: {e}")
else:
    print("❌ OpenAI: Chưa cấu hình OPENAI_API_KEY trong file .env")

# 3. Test kết nối đến Anthropic (Claude-Sonnet-4.5)
anthropic_key = os.getenv("ANTHROPIC_API_KEY")
if anthropic_key:
    try:
        anthropic_client = Anthropic(api_key=anthropic_key)
        anthropic_response = anthropic_client.messages.create(
            model="claude-sonnet-4-5", # Bám sát model trong proposal §5.3
            max_tokens=5,
            messages=[{"role": "user", "content": "Ping"}]
        )
        print("✅ Anthropic (claude-sonnet-4-5): KẾT NỐI THÀNH CÔNG!")
    except Exception as e:
        print(f"❌ Anthropic Lỗi: {e}")
else:
    print("❌ Anthropic: Chưa cấu hình ANTHROPIC_API_KEY trong file .env")