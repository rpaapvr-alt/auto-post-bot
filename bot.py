import os
import requests
import urllib.parse
import random

def run():
    # 1. Загружаем ключи
    api_key = os.getenv("GEMINI_API_KEY")
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("CHAT_ID")

    if not api_key or not token or not chat_id:
        print("Ошибка: Ключи не найдены!")
        return

    # 2. УМНЫЙ ПОИСК МОДЕЛИ (как в прошлый раз)
    try:
        list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
        models_data = requests.get(list_url).json()
        # Ищем любую модель gemini, которая умеет генерировать контент
        model_name = next(
            m['name'] for m in models_data['models'] 
            if 'generateContent' in m['supportedGenerationMethods'] and 'gemini' in m['name']
        )
        print(f"Используем модель: {model_name}")
    except Exception as e:
        print(f"Не удалось найти модель автоматически: {e}")
        model_name = "models/gemini-1.5-flash-latest" # Запасной вариант

    # 3. РАНДОМ ТЕМ (чтобы не было пауков)
    topics = ["космос", "океан", "мозг", "история", "биология", "технологии", "животные"]
    random_topic = random.choice(topics)

    # 4. ЗАПРОС К GEMINI
    url = f"https://generativelanguage.googleapis.com/v1beta/{model_name}:generateContent?key={api_key}"
    
    prompt_text = (
        f"Напиши один короткий редкий научный факт про {random_topic} на русском с эмодзи. "
        "НЕ ПИШИ про пауков во сне и другие баяны. Будь оригинален. "
        "В конце поставь символ | и напиши короткий английский промпт для киберпанк картинки."
    )
    
    payload = {"contents": [{"parts":[{"text": prompt_text}]}]}
    
    res = requests.post(url, json=payload)
    res_data = res.json()

    if 'candidates' not in res_data:
        print(f"Gemini Error: {res_data}")
        return

    try:
        full_text = res_data['candidates'][0]['content']['parts'][0]['text']
        if "|" in full_text:
            fact, img_p = full_text.split("|", 1)
        else:
            fact, img_p = full_text, "cyberpunk science concept"
    except Exception as e:
        print(f"Ошибка разбора текста: {e}")
        return

    # 5. КАРТИНКА И ОТПРАВКА
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(img_p.strip())}?seed={os.urandom(4).hex()}"
    
    r = requests.post(f"https://api.telegram.org/bot{token}/sendPhoto", data={
        "chat_id": chat_id, 
        "caption": fact.strip()[:1024], 
        "photo": img_url
    })
    print(f"Telegram Result: {r.text}")

if __name__ == "__main__":
    run()
