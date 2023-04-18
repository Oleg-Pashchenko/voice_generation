import threading
from multiprocessing.pool import Pool

from interface import main as interface
from database import google as db
from database.models import CreationTask, RequestData
from services import azuresp, yandex, google, zvukogram
from misc import segmentation, filestructure
import multiprocessing
import shutil
import os
from misc.Event import event

def get_request_data(task: CreationTask) -> list[RequestData]:
    response = []
    for i, v in enumerate(task.text):
        response.append(RequestData(
            index=i,
            text=v,
            task=task
        ))
    return response


def get_request_function(task: CreationTask):
    if task.voice.service == 'Microsoft':
        return azuresp.create
    elif task.voice.service == 'Yandex':
        return yandex.create
    elif task.voice.service == 'Google':
        return google.create
    elif task.voice.service == 'Zvukogram':
        return zvukogram.create


def download_mp3s(tasks: list[CreationTask]):
    for index, task in enumerate(tasks):
        print('Началась обработка языка:', task.voice.language)
        rd: list[RequestData] = get_request_data(task)
        func = get_request_function(task)
        with Pool(len(rd)) as p:
            p.map(func, rd)
        event.set()



def get_status_texts() -> list[str]:
    tasks: list[CreationTask] = db.get_tasks()
    response = []
    for index, task in enumerate(tasks):
        response.append(f"[{len(response) + 1} / {len(tasks)}] Загрузка дорожки {task.voice.language}")
    response.append(f'Обработка дорожек')
    return response


def start_app():
    filestructure.prepare_structure()
    tasks: list[CreationTask] = db.get_tasks()
    download_mp3s(tasks)
    segmentation.start(tasks)


def main():
    interface.main()

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
