import os
import shutil


def prepare_structure():
    try:
        shutil.rmtree('temp')
    except Exception as e:
        print(e)
    try:
        shutil.rmtree('res')
    except:
        pass
    os.mkdir('temp')
    os.mkdir('res')