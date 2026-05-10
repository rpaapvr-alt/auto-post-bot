import os, requests

def run():
    api_key = os.getenv("GEMINI_API_KEY")
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("CHAT_ID")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    payload = {"contents": [{"parts":[{"text": "Напиши один короткий интересный факт на русском."}]}]}
    
    res = requests.post(url, json=payload)
    data = res.json()

    # Если Гугл прислал ошибку, мы её увидим в логах
    if 'error' in data:
        print(f"Google API Error: {data['error']['message']}")
        return

    try:
        fact = data['candidates'][0]['content']['parts'][0]['text']
        img_url = "https://image.pollinations.ai/prompt/cyberpunk%20science?width=1024&height=1024"
        
        r = requests.post(f"https://api.telegram.org/bot{token}/sendPhoto", data={
            "chat_id": chat_id, "caption": fact, "photo": img_url
        })
        print(f"Telegram Response: {r.text}")
    except Exception as e:
        print(f"Parsing error: {e}")
        print(f"Full Google Response: {data}")

if __name__ == "__main__":
    run()
