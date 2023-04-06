import os

from mutagen.mp3 import MP3


def get_filenames(name):
    filenames = os.listdir('res/')
    res = []
    for filename in filenames:
        if name in filename:
            res.append(filename)
    res.sort()
    return res

def show_length():
    filenames = get_filenames('.mp3')
    response = []
    for filename in filenames:
        audio = MP3(f"res/{filename}")
        length_in_seconds = audio.info.length
        response.append([length_in_seconds, filename])
    response.sort()
    print(*response, sep='\n')


show_length()
