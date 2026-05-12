import os
import telebot
import requests

# ТВОИ ДАННЫЕ (ВСТАВЬ СВОИ КЛЮЧИ ТУТ)
TOKEN = '8940019675:AAGojwCM2sTvuTBOAk1XiIeFJgFSwxCxLxw'
GEMINI_KEY = "AIzaSyBDT_-Grx3oRArUSTogea0jjknme-5ST-E"

bot = telebot.TeleBot(TOKEN)

def get_ai_translation(text):
    # Используем стабильный эндпоинт с авто-выбором модели
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_KEY}"
    
    data = {
        "contents": [{
            "parts": [{"text": f"Ты — профессиональный ИИ-переводчик. Переведи текст художественно и грамотно. Если текст на русском — на английский, если на английском — на русский. Текст: '{text}'"}]
        }]
    }

    try:
        response = requests.post(url, json=data, timeout=10)
        res_json = response.json()

        # Проверка ошибок от Google
        if "error" in res_json:
            error_msg = res_json['error'].get('message', 'Unknown Error')
            return f"Ошибка Google API: {error_msg}"

        # Возвращаем перевод
        return res_json['candidates'][0]['content']['parts'][0]['text']
    
    except Exception as e:
        return f"Ошибка кода: {str(e)}"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Здорово! Я твой личный ИИ-переводчик. 🌍\nПросто напиши мне фразу, и я её переведу.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Сначала отвечаем, что бот думает
    thinking_msg = bot.reply_to(message, "Думаю...")
    
    # Получаем перевод
    translation = get_ai_translation(message.text)
    
    # Редактируем сообщение "Думаю..." на готовый ответ
    bot.edit_message_text(translation, chat_id=message.chat.id, message_id=thinking_msg.message_id)

if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(none_stop=True)
