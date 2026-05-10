import os, requests

def run():
    api_key = os.getenv("GEMINI_API_KEY")
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("CHAT_ID")

    # 1. Просим Gemini придумать факт через прямой запрос
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    payload = {"contents": [{"parts":[{"text": "Напиши один короткий шокирующий факт на русском с эмодзи."}]}]}
    
    res = requests.post(url, json=payload)
    fact = res.json()['candidates'][0]['content']['parts'][0]['text']
    print(f"Gemini said: {fact}")

    # 2. Генерируем картинку
    img_url = f"https://image.pollinations.ai/prompt/cyberpunk%20science%20discovery?width=1024&height=1024"

    # 3. Шлем в Телеграм
    r = requests.post(f"https://api.telegram.org/bot{token}/sendPhoto", data={
        "chat_id": chat_id, "caption": fact, "photo": img_url
    })
    print(f"Telegram Response: {r.text}")

if __name__ == "__main__":
    run()
