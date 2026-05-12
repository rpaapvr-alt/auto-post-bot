import os
import telebot
import requests

# Забираем данные из секретов GitHub (env переменные)
TOKEN = os.getenv('BOT_TOKEN')
GEMINI_KEY = os.getenv('GEMINI_KEY')

# Если BOT_TOKEN не в секретах, а в коде, раскомментируй строку ниже и вставь его:
# TOKEN = '8940019675:AAfW_sPDEYI5bhTnhXQLu41dhalGjYOAucw'

bot = telebot.TeleBot(TOKEN)

def get_ai_translation(text):
    # Прямой запрос к стабильной версии API v1
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={GEMINI_KEY}"
    
    data = {
        "contents": [{
            "parts": [{"text": f"Ты — профессиональный переводчик. Переведи текст: '{text}'. Если он на русском — на английский, если на английском — на русский."}]
        }]
    }

    try:
        response = requests.post(url, json=data, timeout=10)
        res_json = response.json()

        # Если перевод успешен
        if "candidates" in res_json:
            return res_json['candidates'][0]['content']['parts'][0]['text']
        
        # Если Google вернул ошибку, выводим её ПОЛНОСТЬЮ для отладки
        return f"⚠ Диагностика Google: {str(res_json)}"
    
    except Exception as e:
        return f"❌ Ошибка связи: {str(e)}"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Здорово! Бот на секретных ключах запущен. Пиши фразу для перевода! 🚀")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Бот сначала пишет статус, а потом меняет его на ответ
    status_msg = bot.reply_to(message, "⏳ Анализирую запрос через защищенный шлюз...")
    
    translation = get_ai_translation(message.text)
    
    bot.edit_message_text(translation, chat_id=message.chat.id, message_id=status_msg.message_id)

if __name__ == '__main__':
    print("Бот запущен и ждет сообщений...")
    bot.polling(none_stop=True)
