import os
import requests
import google.generativeai as genai

# Подключаем ключи из настроек GitHub
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
token = os.getenv("TELEGRAM_TOKEN")
chat_id = os.getenv("CHAT_ID")

def run():
    # Используем бесплатную модель Flash
   model = genai.GenerativeModel('gemini-1.5-flash-latest')
    
    # 1. Генерируем текст факта
    prompt = "Напиши один короткий, шокирующий факт о мире на русском языке. Используй эмодзи. Сделай текст интересным для молодежи."
    response = model.generate_content(prompt)
    fact = response.text
    
    # 2. Генерируем промпт для картинки на английском
    img_prompt_req = model.generate_content(f"Describe this fact in 7 English words for an image: {fact}")
    img_description = img_prompt_req.text.replace(" ", "%20")
    
    # Ссылка на бесплатную генерацию картинок (без ключей)
    img_url = f"https://image.pollinations.ai/prompt/{img_description}?width=1024&height=1024&nologo=true"
    
    # 3. Отправляем всё это в твой Telegram канал
    requests.post(f"https://api.telegram.org/bot{token}/sendPhoto", data={
        "chat_id": chat_id,
        "caption": fact,
        "photo": img_url
    })

if __name__ == "__main__":
    run()
