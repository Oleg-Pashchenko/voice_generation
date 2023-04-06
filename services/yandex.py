import json

import requests
import os

API_KEY = 'AQVNyVN0YIKksLUj_8KZ-XJ-S9Cl-6xv8LLQYTs0'


def create(task):
    url = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'
    headers = {
        'Authorization': f'Api-Key {API_KEY}',
    }
    data = {
        'text': task.text,
        'lang': 'ru-RU',
        'voice': 'alena',
        'speed': '1.0',
        'format': 'oggopus'
    }
    response = requests.post(url, headers=headers, data=data)
    with open('audio.ogg', 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)


