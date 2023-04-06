import os
import time

from database.models import CreationTask
from misc.secrets import secret_info
import requests
from multiprocessing import Pool



def f(task):
    try:
        text = task[1]
        index = task[2]
        task =  task[0]
        if task.voice.emotion not in ['good', 'evil', 'neutral']:
            task.voice.emotion = 'good'
        email = 'distribution@guru.markets'
        response = requests.post(
            url='https://zvukogram.com/index.php?r=api/longtext',
            data={
                'token': secret_info.ZVUKOGRAM_API_KEY,
                'email': email,
                'voice': task.voice.speaker,
                'text': text,
                'format': 'mp3',
                'speed': task.voice.speed,
                'pitch': task.voice.tone,
                'emotion': task.voice.emotion
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
                with open(f'temp/{index}_part_{task.audio_name}', 'wb') as f:  # TODO: auto create dir
                    f.write(doc.content)
                break
            elif response2['status'] != '0':
                break
            time.sleep(3)
    except Exception as e:
        print("Exception:", e)

def create(t: CreationTask):
    print("Обработка Zvukogram.")
    arr = []
    count = 0
    for i in t.text:
        count += 1
        arr.append([t, i, count])
    with Pool(len(arr)) as p:
        p.map(f, arr)

