import os
import requests
import urllib.parse
import random

def run():
    # 1. Загружаем секреты
    api_key = os.getenv("GEMINI_API_KEY")
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("CHAT_ID")

    if not api_key or not token or not chat_id:
        print("Ошибка: Ключи не найдены в Secrets!")
        return

    # 2. Список тем, чтобы факты не повторялись
    topics = [
        "глубоководные существа", "тайны космоса", "необычная биология", 
        "квантовая физика", "странные исторические факты", "генетика", 
        "футурология", "парадоксы времени", "микромир", "неизвестные факты о мозге"
    ]
    random_topic = random.choice(topics)

    # 3. Автоматический поиск рабочей модели
    try:
        list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
        models_data = requests.get(list_url).json()
        model_name = next(m['name'] for m in models_data['models'] if 'generateContent' in m['supportedGenerationMethods'] and 'gemini-1.5' in m['name'])
    except:
        model_name = "models/gemini-1.5-flash"

    # 4. Запрос к Gemini с жестким условием не повторяться
    url = f"https://generativelanguage.googleapis.com/v1beta/{model_name}:generateContent?key={api_key}"
    
    prompt_text = (
        f"Напиши один действительно редкий и шокирующий научный факт на тему '{random_topic}' на русском языке с эмодзи. "
        "НЕ ПИШИ про пауков во сне и другие заезженные мифы. Факт должен быть правдивым. "
        "Затем поставь символ '|' и напиши короткий английский промпт для генерации картинки в стиле киберпанк, "
        "которая визуально передает этот факт."
    )
    
    payload = {"contents": [{"parts":[{"text": prompt_text}]}]}
    
    try:
        res = requests.post(url, json=payload)
        full_response = res.json()['candidates'][0]['content']['parts'][0]['text']
        
        if "|" in full_response:
            fact, img_prompt = full_response.split("|", 1)
        else:
            fact = full_response
            img_prompt = f"cyberpunk {random_topic} futuristic science"
            
    except Exception as e:
        print(f"Ошибка Gemini: {e}")
        return

    # 5. Генерация уникальной картинки
    clean_prompt = urllib.parse.quote(img_prompt.strip().replace("\n", " "))
    seed = os.urandom(4).hex() # Каждый раз новая картинка, даже если промпт похож
    img_url = f"https://image.pollinations.ai/prompt/{clean_prompt}?width=1024&height=1024&seed={seed}&nologo=true"

    # 6. Отправка в Telegram
    tele_url = f"https://api.telegram.org/bot{token}/sendPhoto"
    data = {
        "chat_id": chat_id,
        "caption": fact.strip()[:1024],
        "photo": img_url
    }
    
    response = requests.post(tele_url, data=data)
    print(f"Telegram response: {response.text}")

if __name__ == "__main__":
    run()
