import os
from openai import OpenAI

# 1. Tự động nạp cấu hình từ file .env bảo mật nếu có
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

print("--- KHỞI ĐỘNG KIỂM TRA API (OPENROUTER) ---")

openrouter_key = os.getenv("OPENROUTER_API_KEY")
openrouter_base = os.getenv("OPENROUTER_API_BASE", "https://openrouter.ai/api/v1")
exploration_model = os.getenv("EXPLORATION_MODEL_NAME", "deepseek/deepseek-chat:free")
fixer_model = os.getenv("FIXER_MODEL_NAME", "meta-llama/llama-3.3-70b-instruct:free")

if not openrouter_key:
    print("❌ Chưa cấu hình OPENROUTER_API_KEY!")
else:
    client = OpenAI(
        api_key=openrouter_key,
        base_url=openrouter_base,
        default_headers={
            "HTTP-Referer": "https://github.com/lctx9/group4",
            "X-Title": "RT-SWT-005 Group 4 Project"
        }
    )

    # Test Exploration Agent
    print(f"🤖 Đang kiểm tra Exploration Agent ({exploration_model})...")
    try:
        resp = client.chat.completions.create(
            model=exploration_model,
            messages=[{"role": "user", "content": "Ping"}],
            max_tokens=5
        )
        print(f"✅ Exploration Agent: KẾT NỐI THÀNH CÔNG! Phản hồi: {resp.choices[0].message.content.strip()}")
    except Exception as e:
        print(f"❌ Exploration Agent Lỗi: {e}")

    # Test Fixer Agent
    print(f"🤖 Đang kiểm tra Fixer Agent ({fixer_model})...")
    try:
        resp = client.chat.completions.create(
            model=fixer_model,
            messages=[{"role": "user", "content": "Ping"}],
            max_tokens=5
        )
        print(f"✅ Fixer Agent: KẾT NỐI THÀNH CÔNG! Phản hồi: {resp.choices[0].message.content.strip()}")
    except Exception as e:
        print(f"❌ Fixer Agent Lỗi: {e}")