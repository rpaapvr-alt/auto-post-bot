import os
import telebot
import requests

# ТВОИ ДАННЫЕ
TOKEN = '8940019675:AAGojwCM2sTvuTBOAk1XiIeFJgFSwxCxLxw'
GEMINI_KEY = "AIzaSyBDT_-Grx3oRArUSTogea0jjknme-5ST-E"

bot = telebot.TeleBot(TOKEN)

def get_ai_translation(text):
    # Список моделей по приоритету: сначала самая быстрая, потом надежная
    models = ["gemini-1.5-flash-latest", "gemini-1.5-flash", "gemini-pro"]
    
    for model_name in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={GEMINI_KEY}"
        data = {
            "contents": [{
                "parts": [{"text": f"Переведи художественно. Если русский — на английский, если английский — на русский: '{text}'"}]
            }]
        }

        try:
            response = requests.post(url, json=data, timeout=10)
            res_json = response.json()

            # Если модель найдена и ответила — возвращаем текст
            if "candidates" in res_json:
                return res_json['candidates'][0]['content']['parts'][0]['text']
            
            # Если ошибка "не найдено", идем к следующей модели в списке
            if "error" in res_json and "not found" in res_json['error'].get('message', '').lower():
                continue
                
            if "error" in res_json:
                return f"Ошибка API: {res_json['error'].get('message')}"

        except Exception as e:
            continue # Пробуем следующую модель при сбое связи
            
    return "Не удалось подобрать рабочую модель Gemini. Проверь ключ."

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Здорово! Я умный переводчик. Пиши фразу!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    thinking = bot.reply_to(message, "Подбираю модель и перевожу...")
    translation = get_ai_translation(message.text)
    bot.edit_message_text(translation, chat_id=message.chat.id, message_id=thinking.message_id)

if __name__ == '__main__':
    bot.polling(none_stop=True)
