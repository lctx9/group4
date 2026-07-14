import os
from openai import OpenAI

# 1. Tự động nạp cấu hình từ file .env bảo mật nếu có
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

print("--- KHỞI ĐỘNG KIỂM TRA API GATE E3 (HỖ TRỢ GEMINI + OPENROUTER + DEEPSEEK) ---")

# 2. Test kết nối đến Exploration Agent qua OpenRouter (DeepSeek-V3)
openrouter_key = os.getenv("OPENROUTER_API_KEY")
openrouter_base = os.getenv("OPENROUTER_API_BASE", "https://openrouter.ai/api/v1")
exploration_model = os.getenv("EXPLORATION_MODEL_NAME", "deepseek/deepseek-chat")

if openrouter_key:
    try:
        print(f"🤖 Đang kiểm tra Exploration Agent (OpenRouter) tại: {openrouter_base}...")
        openrouter_client = OpenAI(
            api_key=openrouter_key, 
            base_url=openrouter_base,
            default_headers={
                "HTTP-Referer": "https://github.com/lctx9/group4",
                "X-Title": "RT-SWT-005 Group 4 Project"
            }
        )
        response = openrouter_client.chat.completions.create(
            model=exploration_model,
            messages=[{"role": "user", "content": "Ping"}],
            max_tokens=5
        )
        print(f"✅ OpenRouter ({exploration_model}): KẾT NỐI THÀNH CÔNG! Phản hồi: {response.choices[0].message.content.strip()}")
    except Exception as e:
        print(f"❌ OpenRouter Lỗi: {e}")
else:
    print(f"⚠️ OpenRouter: Chưa cấu hình OPENROUTER_API_KEY.")

# 3. Test kết nối đến Gemini API (nếu được cấu hình trực tiếp)
gemini_key = os.getenv("GEMINI_API_KEY")
gemini_base = os.getenv("GEMINI_API_BASE", "https://generativelanguage.googleapis.com/v1beta/openai/")
gemini_model = os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-flash") # Dùng gemini-2.5-flash làm mặc định

if gemini_key:
    try:
        print(f"🤖 Đang kiểm tra Code Action Fixer (Gemini) tại: {gemini_base}...")
        gemini_client = OpenAI(api_key=gemini_key, base_url=gemini_base)
        response = gemini_client.chat.completions.create(
            model=gemini_model,
            messages=[{"role": "user", "content": "Ping"}],
            max_tokens=5
        )
        print(f"✅ Gemini ({gemini_model}): KẾT NỐI THÀNH CÔNG! Phản hồi: {response.choices[0].message.content.strip()}")
    except Exception as e:
        print(f"❌ Gemini Lỗi: {e}")
else:
    print(f"⚠️ Gemini: Chưa cấu hình GEMINI_API_KEY.")

# 4. Test kết nối đến DeepSeek Native
deepseek_key = os.getenv("DEEPSEEK_API_KEY")
deepseek_base = os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com/v1")
deepseek_model = os.getenv("DEEPSEEK_MODEL_NAME", "deepseek-reasoner")

if deepseek_key:
    try:
        print(f"🤖 Đang kiểm tra Code Action Fixer (DeepSeek Native) tại: {deepseek_base}...")
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
    print(f"⚠️ DeepSeek Native: Chưa cấu hình DEEPSEEK_API_KEY.")