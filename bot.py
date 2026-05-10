import os, requests
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
token = os.getenv("TELEGRAM_TOKEN")
chat_id = os.getenv("CHAT_ID")

def run():
    # Пробуем разные варианты названий модели
    for model_name in ['gemini-1.5-flash', 'gemini-1.5-flash-latest', 'gemini-pro']:
        try:
            model = genai.GenerativeModel(model_name)
            fact = model.generate_content("Напиши один короткий шокирующий факт на русском с эмодзи.").text
            img_p = model.generate_content(f"Short image description in English: {fact}").text
            img_url = f"https://image.pollinations.ai/prompt/{img_p.replace(' ', '%20')}?width=1024&height=1024"
            
            r = requests.post(f"https://api.telegram.org/bot{token}/sendPhoto", data={
                "chat_id": chat_id, "caption": fact, "photo": img_url
            })
            print(f"Success with {model_name}! Status: {r.status_code}")
            return # Если получилось, выходим из цикла
        except Exception as e:
            print(f"Failed with {model_name}: {e}")

if __name__ == "__main__":
    run()
