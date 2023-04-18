import os
import time

from database.models import CreationTask, RequestData
from misc.secrets import secret_info
import requests
from multiprocessing import Pool



def create(rd: RequestData):
    try:
        if rd.task.voice.emotion not in ['good', 'evil', 'neutral']:
            rd.task.voice.emotion = 'good'
        email = 'distribution@guru.markets'
        response = requests.post(
            url='https://zvukogram.com/index.php?r=api/longtext',
            data={
                'token': secret_info.ZVUKOGRAM_API_KEY,
                'email': email,
                'voice': rd.task.voice.speaker,
                'text': rd.text,
                'format': 'mp3',
                'speed': rd.task.voice.speed,
                'pitch': rd.task.voice.tone,
                'emotion': rd.task.voice.emotion
            }
        ).json()

        while True:
            response2 = requests.post(
                url='https://zvukogram.com/index.php?r=api/result',
                data={
                    'token': secret_info.ZVUKOGRAM_API_KEY,
                    'email': email,
                    'id': response['id']
                }
            ).json()
            if response2['status'] == '1':
                doc = requests.get(response2['file'])
                with open(f'temp/{rd.index}_part_{rd.task.audio_name}', 'wb') as f:
                    f.write(doc.content)
                break
            elif response2['status'] != '0':
                break
            time.sleep(3)
    except Exception as e:
        print("Exception:", e)

