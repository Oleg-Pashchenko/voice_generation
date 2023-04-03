import os
from misc.secrets import secret_info
import requests
email = 'distribution@guru.markets'
response = requests.post(
    url='https://zvukogram.com/index.php?r=api/longtext',
    data={
        'token': secret_info.ZVUKOGRAM_API_KEY,
        'email': email,
        'voice': 'Владимир',
        'text': 'Текст который будет озвучен',
    } #         'format': '', 'speed': '', 'pitch': '','emotion': ''
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
        print(response2['file'])
    elif response2['status'] == '0':
        print('in process')
    else:
        print('error')