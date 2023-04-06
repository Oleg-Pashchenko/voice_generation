from database import google as db
from services import azuresp, yandex, google, zvukogram
from misc import segmentation
from multiprocessing import freeze_support

def start_app():
    tasks = db.get_tasks()
    count = 0
    for task in tasks:
        count += 1
        print(f'№{count} {task.audio_name}')
        if task.voice.service == 'Microsoft':
            azuresp.create(task)
        elif task.voice.service == 'Yandex':
            yandex.create(task)
        elif task.voice.service == 'Google':
            google.create(task)
        elif task.voice.service == 'Zvukogram':
            zvukogram.create(task)
    segmentation.start(tasks)

if __name__ == "__main__":
    freeze_support()
    start_app()

