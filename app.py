from flask import Flask, render_template, request
import requests
import random

# Список API для случайных цитат
QUOTE_APIS = [
    'https://zenquotes.io/api/random',
    'https://api.api-ninjas.com/v1/quotes',  # Требует токен авторизации
    'https://quoteslate.vercel.app'
]

app = Flask(__name__)


@app.route('/')
def index():
    quote_api = random.choice(QUOTE_APIS)

    if quote_api == QUOTE_APIS[1]:  # Если выбран api-ninjas, используем ключ
        headers = {'X-Api-Key': 'YOUR_API_KEY_HERE'}
        response = requests.get(quote_api, headers=headers).json()
        return render_template('index.html', quote=f"{response['quote']} — {response['author']}")
    else:
        response = requests.get(quote_api).json()

        # Обработка различных форматов ответа от разных API
        if isinstance(response, list):
            data = response[0]
            return render_template('index.html', quote=f"{data['q']} — {data['a']}")
        elif isinstance(response, dict):
            return render_template('index.html', quote=f"{response['text']} — {response['author']}")
        else:
            return render_template('index.html', quote="Ошибка загрузки цитаты")


if __name__ == '__main__':
    app.run(debug=True)