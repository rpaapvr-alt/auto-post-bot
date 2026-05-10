import os, requests
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
token = os.getenv("TELEGRAM_TOKEN")
chat_id = os.getenv("CHAT_ID")

def run():
    for model_name in ['gemini-1.5-flash', 'gemini-pro']:
        try:
            model = genai.GenerativeModel(model_name)
            fact = model.generate_content("Напиши один шокирующий факт на русском с эмодзи.").text
            img_url = f"https://image.pollinations.ai/prompt/cyberpunk%20style%20science?width=1024&height=1024"
            
            payload = {"chat_id": chat_id, "caption": fact, "photo": img_url}
            r = requests.post(f"https://api.telegram.org/bot{token}/sendPhoto", data=payload)
            
            print(f"Model: {model_name}")
            print(f"Telegram Response: {r.text}") # Это покажет РЕАЛЬНУЮ причину
            return
        except Exception as e:
            print(f"Error with {model_name}: {e}")

if __name__ == "__main__":
    run()
