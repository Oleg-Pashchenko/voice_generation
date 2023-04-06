from mutagen.mp3 import MP3
import os

from database.google import write_stats
from database.models import CreationTask
from pydub import AudioSegment


def get_filenames(name):
    filenames = os.listdir('temp/')
    res = []
    for filename in filenames:
        if name in filename:
            res.append(filename)
    res = sorted(res, key=sort_key_func)
    return res
from mutagen.mp3 import MP3
from mutagen.id3 import ID3

def get_language_length(name):
    filenames = get_filenames(name)
    response, summary = {}, 0
    r = []
    for filename in filenames:
        audio = MP3(f"temp/{filename}", ID3=ID3)
        length_in_seconds = audio.info.length
        r.append(length_in_seconds)
        summary += length_in_seconds
        response[filename] = length_in_seconds
    return summary, response, r



def short_pauses(tasks: list[CreationTask]):
    for task in tasks:
        filenames = get_filenames(task.audio_name)
        for filename in filenames:
            print(filename)
            try:
                audio = AudioSegment.from_mp3(f'temp/{filename}')
                audio_without_silence = audio.strip_silence(silence_len=200, silence_thresh=-50, padding=5)
                audio_with_new_silence = audio_without_silence + AudioSegment.silent(duration=200)
                audio_with_new_silence.export(f'temp/{filename}', format="mp3")
            except:
                pass


def choose_etalon(tasks):
    result = []
    etalon = []
    for task in tasks:
        length, file_by_file_info, r = get_language_length(task.audio_name)
        result.append([length, file_by_file_info, task.audio_name])
        if len(etalon) == 0:
            etalon = list(r)
            continue
        try:
            for i in range(len(etalon)):
                if etalon[i] < r[i]:
                    etalon[i] = r[i]
        except:
            pass

    result.sort()
    return result, etalon

def sort_key_func(s):
    return int(s.split("_")[0])


def concatenate_files(result, timings):
    c = 0
    for voice in result:
        index = -1
        c += 1
        combined_sound = AudioSegment.silent(duration=0)
        print(f"{c} / {len(result)}")
        for k in sorted(voice[1].keys(), key=sort_key_func):
            index += 1
            new_voice = AudioSegment.from_file(f"temp/{k}", format="mp3")
            silence = AudioSegment.silent(duration=timings[index] * 1000 - new_voice.duration_seconds * 1000)
            new_voice += silence
            combined_sound += new_voice
        try:
            combined_sound.export(f"res/{'_'.join(k.split('_')[2::])}", format="mp3")
        except:
            pass


def start(tasks: list[CreationTask]):
    short_pauses(tasks)
    result, etalon = choose_etalon(tasks)
    print(sum(etalon))
    concatenate_files(result, etalon)
    write_stats(result)

