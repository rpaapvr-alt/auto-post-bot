import os, requests

def run():
    api_key = os.getenv("GEMINI_API_KEY")
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("CHAT_ID")

    # Используем стабильную версию v1 и модель без лишних букв
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{"text": "Напиши один короткий шокирующий факт на русском с эмодзи."}]
        }]
    }
    
    res = requests.post(url, json=payload)
    data = res.json()

    if 'error' in data:
        print(f"Google API Error: {data['error']['message']}")
        return

    try:
        fact = data['candidates'][0]['content']['parts'][0]['text']
        # Картинка-заглушка, чтобы точно сработало
        img_url = "https://image.pollinations.ai/prompt/cyberpunk%20science%20space?width=1024&height=1024"
        
        r = requests.post(f"https://api.telegram.org/bot{token}/sendPhoto", data={
            "chat_id": chat_id, 
            "caption": fact, 
            "photo": img_url
        })
        print(f"Telegram Status: {r.status_code}")
        print(f"Telegram Response: {r.text}")
    except Exception as e:
        print(f"Error: {e}")
        print(f"Full Data: {data}")

if __name__ == "__main__":
    run()
