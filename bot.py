import os, requests

def run():
    api_key = os.getenv("GEMINI_API_KEY")
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("CHAT_ID")

    # Сначала узнаем, какая модель тебе доступна
    list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    models_data = requests.get(list_url).json()
    
    # Берем самую первую модель, которая умеет генерировать контент
    model_name = next(m['name'] for m in models_data['models'] if 'generateContent' in m['supportedGenerationMethods'])
    print(f"Using model: {model_name}")

    # Теперь шлем запрос именно к ней
    url = f"https://generativelanguage.googleapis.com/v1beta/{model_name}:generateContent?key={api_key}"
    payload = {"contents": [{"parts":[{"text": "Напиши один короткий шокирующий факт на русском с эмодзи."}]}]}
    
    res = requests.post(url, json=payload)
    fact = res.json()['candidates'][0]['content']['parts'][0]['text']

    img_url = "https://image.pollinations.ai/prompt/cyberpunk%20science?width=1024&height=1024"
    
    r = requests.post(f"https://api.telegram.org/bot{token}/sendPhoto", data={
        "chat_id": chat_id, "caption": fact, "photo": img_url
    })
    print(f"Telegram Response: {r.text}")

if __name__ == "__main__":
    run()
