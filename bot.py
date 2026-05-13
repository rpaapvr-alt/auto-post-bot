import requests
import os
import json

# Конфигурация
API_KEY = os.getenv("GEMINI_API_KEY")
BASE_URL = "https://generativelanguage.googleapis.com/v1beta"

def get_working_model():
    """Автоматически находит рабочую версию модели в твоем аккаунте"""
    list_url = f"{BASE_URL}/models?key={API_KEY}"
    try:
        res = requests.get(list_url)
        if res.status_code != 200:
            print(f"Не удалось получить список моделей: {res.status_code}")
            return "gemini-1.5-flash" # Фолбэк на стандарт
            
        models_data = res.json()
        # Ищем сначала 1.5 flash, потом просто flash, потом pro
        priority = ["models/gemini-1.5-flash", "models/gemini-1.5-pro", "models/gemini-pro"]
        
        available_models = [m['name'] for m in models_data.get('models', [])]
        
        for p in priority:
            if p in available_models:
                print(f"Автоопределение: выбрана модель {p}")
                return p
        
        # Если ничего из приоритетов не нашли, берем первую попавшуюся генеративную
        return available_models[0] if available_models else "gemini-1.5-flash"
    except Exception as e:
        print(f"Ошибка при автоопределении модели: {e}")
        return "gemini-1.5-flash"

def run():
    model_id = get_working_model()
    # model_id уже содержит префикс 'models/', так что в URL вставляем аккуратно
    clean_model_id = model_id.split('/')[-1]
    
    gen_url = f"{BASE_URL}/models/{clean_model_id}:generateContent?key={API_KEY}"
    
    payload = {
        "contents": [{
            "parts": [{"text": "Напиши один короткий и офигенный факт для телеграм канала на русском языке."}]
        }]
    }
    
    headers = {'Content-Type': 'application/json'}
    
    try:
        print(f"Отправка запроса к {clean_model_id}...")
        res = requests.post(gen_url, headers=headers, json=payload)
        
        if res.status_code != 200:
            print(f"Ошибка генерации (Статус {res.status_code}): {res.text}")
            return

        res_data = res.json()
        if 'candidates' in res_data:
            fact = res_data['candidates'][0]['content']['parts'][0]['text']
            print(f"Результат: {fact}")
            # ТУТ ТВОЙ КОД ОТПРАВКИ В ТГ
        else:
            print("Ответ пустой, проверь логи в AI Studio.")
            
    except Exception as e:
        print(f"Критический сбой: {e}")

if __name__ == "__main__":
    run()
