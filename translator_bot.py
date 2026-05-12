import os
import telebot
import requests

# Вставь сюда токен, который тебе дал @BotFather
TOKEN ='8940019675:AAFw_sPDEYI5bhTnhXQLu41dhalGjYOAucw'
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

bot = telebot.TeleBot(TOKEN)

def get_ai_translation(text):
    # Используем актуальную модель Gemini
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_KEY}"
    
    # Промпт для качественного перевода
    prompt = (
        f"Ты — профессиональный ИИ-переводчик. Твоя задача: "
        f"1. Если текст на русском — переведи его на английский. "
        f"2. Если текст на английском — переведи его на русский. "
        f"Переводи художественно и грамотно. "
        f"Текст для перевода: '{text}'"
    )
    
    payload = {"contents": [{"parts":[{"text": prompt}]}]}
    
    try:
        res = requests.post(url, json=payload)
        res_data = res.json()
        # Извлекаем только текст перевода
        return res_data['candidates'][0]['content']['parts'][0]['text'].strip()
    except Exception as e:
        print(f"Ошибка Gemini: {e}")
        return "Уппс, нейронка занята. Попробуй через минуту! 🤖"

# Ответ на команду /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Здорово! Я твой личный ИИ-переводчик. 🌍\nПросто напиши мне фразу на русском или английском, и я её переведу.")

# Обработка всех входящих сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Бот показывает статус "печать", чтобы было понятно, что он думает
    bot.send_chat_action(message.chat.id, 'typing')
    
    result = get_ai_translation(message.text)
    bot.reply_to(message, result)

if __name__ == "__main__":
    print("Бот-переводчик запущен и ждет сообщений...")
    bot.infinity_polling()
