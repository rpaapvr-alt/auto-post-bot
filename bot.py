import os
import requests
import urllib.parse
import random

def run():
    api_key = os.getenv("GEMINI_API_KEY")
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("CHAT_ID")

    topics = ["космос", "океан", "мозг человека", "древние животные", "технологии будущего"]
    random_topic = random.choice(topics)

    # 1. Запрос к Gemini
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    prompt_text = f"Напиши один короткий научный факт про {random_topic} на русском с эмодзи. В конце через символ | напиши короткий промпт для картинки на английском."
    
    payload = {"contents": [{"parts":[{"text": prompt_text}]}]}
    
    res = requests.post(url, json=payload)
    res_data = res.json()

    # ПРОВЕРКА: если Gemini выдала ошибку
    if 'candidates' not in res_data:
        print(f"Gemini Error: {res_data}") # Это покажет нам реальную причину в логах
        return

    try:
        full_text = res_data['candidates'][0]['content']['parts'][0]['text']
        if "|" in full_text:
            fact, img_p = full_text.split("|", 1)
        else:
            fact, img_p = full_text, "cyberpunk science concept"
    except Exception as e:
        print(f"Parsing error: {e}")
        return

    # 2. Картинка
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(img_p.strip())}?seed={os.urandom(4).hex()}"

    # 3. Отправка
    r = requests.post(f"https://api.telegram.org/bot{token}/sendPhoto", data={
        "chat_id": chat_id, "caption": fact.strip(), "photo": img_url
    })
    print(f"Telegram: {r.text}")

if __name__ == "__main__":
    run()
