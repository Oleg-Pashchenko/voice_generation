import json
import requests
import os

from database.models import CreationTask, RequestData
from misc import secrets

API_KEY = secrets.secret_info.YANDEX_API_KEY


def create(rd: RequestData):
    url = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'
    headers = {
        'Authorization': f'Api-Key {API_KEY}',
    }
    data = {
        'text': rd.text,
        'lang': rd.task.voice.language,
        'voice': rd.task.voice.speaker,
        'speed': rd.task.voice.speed,
        'format': 'mp3'
    }
    response = requests.post(url, headers=headers, data=data)
    with open(f'temp/{rd.index}_part_{rd.task.audio_name}', 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)


