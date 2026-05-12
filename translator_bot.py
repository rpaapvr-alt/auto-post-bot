import os
import telebot
import requests

TOKEN = os.getenv('BOT_TOKEN')
GEMINI_KEY = os.getenv('GEMINI_KEY')

bot = telebot.TeleBot(TOKEN)

def get_working_model():
    """Автоматически находит рабочую модель Gemini"""
    list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={GEMINI_KEY}"
    try:
        res = requests.get(list_url).json()
        for m in res.get('models', []):
            # Ищем модель, которая умеет генерировать контент и не является 'vision'
            if 'generateContent' in m.get('supportedGenerationMethods', []) and 'vision' not in m['name']:
                return m['name']
        return "models/gemini-1.5-flash" # Запасной вариант
    except:
        return "models/gemini-1.5-flash"

def get_ai_translation(text):
    model_name = get_working_model()
    url = f"https://generativelanguage.googleapis.com/v1beta/{model_name}:generateContent?key={GEMINI_KEY}"
    
    data = {
        "contents": [{
            "parts": [{"text": f"Переведи текст на противоположный язык (рус/англ): '{text}'. Пиши ТОЛЬКО перевод."}]
        }]
    }

    try:
        response = requests.post(url, json=data, timeout=10)
        res_json = response.json()
        if "candidates" in res_json:
            return res_json['candidates'][0]['content']['parts'][0]['text']
        return f"⚠ Ошибка API: {str(res_json)}"
    except Exception as e:
        return f"❌ Ошибка связи: {str(e)}"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Яна шлюха.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    status_msg = bot.reply_to(message, "⏳ Подключаюсь к лучшему серверу Google...")
    translation = get_ai_translation(message.text)
    bot.edit_message_text(translation, chat_id=message.chat.id, message_id=status_msg.message_id)

if __name__ == '__main__':
    bot.polling(none_stop=True)
