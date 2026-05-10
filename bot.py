import os, requests

def run():
    api_key = os.getenv("GEMINI_API_KEY")
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("CHAT_ID")

    # 1. Спрашиваем список моделей
    list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    models_data = requests.get(list_url).json()
    model_name = next(m['name'] for m in models_data['models'] if 'generateContent' in m['supportedGenerationMethods'])

    url = f"https://generativelanguage.googleapis.com/v1beta/{model_name}:generateContent?key={api_key}"
    
    # 2. Просим Gemini сделать ДВЕ вещи: факт и промпт для картинки на английском
    prompt_text = "Напиши один короткий шокирующий факт на русском с эмодзи. А затем, через символ |, напиши короткий английский промпт для генерации футуристичной картинки к этому факту."
    
    payload = {"contents": [{"parts":[{"text": prompt_text}]}]}
    res = requests.post(url, json=payload)
    full_response = res.json()['candidates'][0]['content']['parts'][0]['text']

    # Разделяем факт и промпт
    if "|" in full_response:
        fact, image_prompt = full_response.split("|")
    else:
        fact = full_response
        image_prompt = "cyberpunk science technology" # Запасной вариант

    print(f"Fact: {fact}")
    print(f"Image Prompt: {image_prompt}")

    # 3. Генерируем картинку по УНИКАЛЬНОМУ промпту
    # Убираем пробелы и лишние символы для ссылки
    clean_prompt = requests.utils.quote(image_prompt.strip())
    img_url = f"https://image.pollinations.ai/prompt/{clean_prompt}?width=1024&height=1024&seed={os.urandom(4).hex()}"

    # 4. Отправка
    r = requests.post(f"https://api.telegram.org/bot{token}/sendPhoto", data={
        "chat_id": chat_id, "caption": fact.strip(), "photo": img_url
    })
    print(f"Telegram Response: {r.text}")

if __name__ == "__main__":
    run()
