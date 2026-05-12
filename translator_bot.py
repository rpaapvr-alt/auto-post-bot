iimport os
import telebot
import requests

# Подтягиваем секреты из GitHub Actions
TOKEN = os.getenv('BOT_TOKEN')
GEMINI_KEY = os.getenv('GEMINI_KEY')

bot = telebot.TeleBot(TOKEN)

def get_ai_translation(text):
    # Используем v1beta и модель gemini-1.5-flash (самая стабильная сейчас)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    
    data = {
        "contents": [{
            "parts": [{"text": f"Ты — профессиональный переводчик. Переведи текст: '{text}'. Если он на русском — на английский, если на английском — на русский. Пиши ТОЛЬКО текст перевода, без лишних слов."}]
        }]
    }

    try:
        response = requests.post(url, json=data, timeout=10)
        res_json = response.json()

        # Проверка на успешный ответ
        if "candidates" in res_json:
            return res_json['candidates'][0]['content']['parts'][0]['text']
        
        # Если что-то не так, выводим техническую инфу (для нас)
        return f"⚠ Ошибка Google API: {res_json.get('error', {}).get('message', 'Неизвестная ошибка')}"
    
    except Exception as e:
        return f"❌ Ошибка связи: {str(e)}"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Здорово! Я твой личный ИИ-переводчик. 🌍\nПросто напиши мне фразу, и я её переведу.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Отправляем временное сообщение, чтобы юзер не думал, что бот завис
    status_msg = bot.reply_to(message, "⏳ Перевожу...")
    
    translation = get_ai_translation(message.text)
    
    # Редактируем то самое временное сообщение, вставляя перевод
    bot.edit_message_text(translation, chat_id=message.chat.id, message_id=status_msg.message_id)

if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(none_stop=True)
