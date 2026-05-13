import os
import requests
import urllib.parse
import random

def run():
    api_key = os.getenv("GEMINI_API_KEY")
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("CHAT_ID")

    if not api_key or not token or not chat_id:
        print("Ошибка: Ключи не найдены!")
        return

    # 1. МАКСИМАЛЬНО РАЗНЫЕ ТЕМЫ
    science_topics = [
        "черные дыры и парадоксы времени", "глубоководные монстры океана", 
        "древние вымершие гиганты", "тайны человеческого подсознания", 
        "микроскопические организмы-экстремофилы", "футуристические гаджеты 22 века",
        "неразгаданные археологические находки", "квантовое бессмертие"
    ]
    
    cat_topics = [
        "дикие предки домашних кошек", "почему кошки ведут себя как жидкость", 
        "мифология кошек в разных странах", "необычные способности кошачьих чувств",
        "редчайшие и странные породы кошек", "коты в открытом космосе (фантастика)"
    ]

    # Шанс 50/50: наука или котики
    if random.choice([True, False]):
        random_topic = random.choice(science_topics)
        style = "научный, шокирующий, киберпанк"
    else:
        random_topic = random.choice(cat_topics)
        style = "забавный, милый, футуристичный"

    # 2. ПОИСК МОДЕЛИ
    try:
        list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
        models_data = requests.get(list_url).json()
        model_name = next(m['name'] for m in models_data['models'] if 'generateContent' in m['supportedGenerationMethods'] and 'gemini' in m['name'])
    except:
       model_name = "gemini-1.5-flash"

    # 3. ЗАПРОС С "ИНЪЕКЦИЕЙ ХАОСА"
    url = f"https://generativelanguage.googleapis.com/v1beta/{model_name}:generateContent?key={api_key}"
    
    # Добавляем случайное число, чтобы ИИ каждый раз менял подачу
    chaos_seed = random.randint(1, 1000)
    
    prompt_text = (
        f"Напиши один уникальный факт на тему '{random_topic}' на русском языке с эмодзи. "
        f"Стиль: {style}. Не используй заезженные факты. Удиви читателя. "
        f"Уникальный идентификатор запроса: {chaos_seed}. "
        "После текста поставь символ '|' и напиши английский промпт для генерации "
        f"картинки, которая передает атмосферу этого факта в стиле {style}."
    )
    
    payload = {"contents": [{"parts":[{"text": prompt_text}]}]}
    
    res = requests.post(url, json=payload)
    res_data = res.json()

    if 'candidates' not in res_data:
        print(f"Gemini Error: {res_data}")
        return

    try:
        full_text = res_data['candidates'][0]['content']['parts'][0]['text']
        fact, img_p = full_text.split("|", 1) if "|" in full_text else (full_text, "futuristic art")
    except Exception as e:
        print(f"Ошибка: {e}")
        return

    # 4. КАРТИНКА И ОТПРАВКА
    # Добавляем seed и в Pollinations, чтобы картинки ВСЕГДА были разными
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(img_p.strip())}?seed={random.randint(1, 999999)}&width=1024&height=1024&nologo=true"
    
    r = requests.post(f"https://api.telegram.org/bot{token}/sendPhoto", data={
        "chat_id": chat_id, 
        "caption": fact.strip()[:1024], 
        "photo": img_url
    })
    print(f"Telegram Result: {r.text}")

if __name__ == "__main__":
    run()
