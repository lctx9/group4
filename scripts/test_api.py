import os
from openai import OpenAI

# 1. Tự động nạp cấu hình từ file .env bảo mật nếu có
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

print("--- KHỞI ĐỘNG KIỂM TRA API GATE E3 (CẬP NHẬT: OPENROUTER + DEEPSEEK) ---")

# 2. Test kết nối đến Exploration Agent qua OpenRouter (DeepSeek)
openrouter_key = os.getenv("OPENROUTER_API_KEY")
openrouter_base = os.getenv("OPENROUTER_API_BASE", "https://openrouter.ai/api/v1")
exploration_model = os.getenv("EXPLORATION_MODEL_NAME", "deepseek/deepseek-chat") # Dùng DeepSeek-V3 qua OpenRouter làm Exploration Agent

if openrouter_key:
    try:
        print(f"🤖 Đang kiểm tra Exploration Agent (DeepSeek qua OpenRouter) tại: {openrouter_base}...")
        # OpenRouter yêu cầu truyền thêm headers (optional nhưng khuyến khích)
        openrouter_client = OpenAI(
            api_key=openrouter_key, 
            base_url=openrouter_base,
            default_headers={
                "HTTP-Referer": "https://github.com/lctx9/group4", # Tên repo của nhóm
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
    print(f"⚠️ OpenRouter: Chưa cấu hình OPENROUTER_API_KEY. Sẽ dùng chế độ giả lập (Mock Mode) khi chạy thực nghiệm.")

# 3. Test kết nối đến Code Action Fixer: DeepSeek V4 Pro (hoặc gọi qua OpenRouter nếu muốn dùng chung)
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
    # Nếu không có key DeepSeek riêng, thử kiểm tra xem có dùng chung OpenRouter để gọi DeepSeek R1/Reasoner không
    if openrouter_key:
        try:
            print(f"🤖 Thử kết nối Code Action Fixer (DeepSeek R1/Reasoner) qua OpenRouter...")
            openrouter_client = OpenAI(api_key=openrouter_key, base_url=openrouter_base)
            response = openrouter_client.chat.completions.create(
                model="deepseek/deepseek-r1", # Hoặc deepseek/deepseek-r1:free / deepseek/deepseek-chat
                messages=[{"role": "user", "content": "Ping"}],
                max_tokens=5
            )
            print(f"✅ OpenRouter (deepseek/deepseek-r1): KẾT NỐI THÀNH CÔNG! Phản hồi: {response.choices[0].message.content.strip()}")
        except Exception as e:
            print(f"❌ Thử kết nối R1 qua OpenRouter Lỗi: {e}")
    else:
        print(f"⚠️ DeepSeek: Chưa cấu hình DEEPSEEK_API_KEY. Sẽ dùng chế độ giả lập (Mock Mode) khi chạy thực nghiệm.")