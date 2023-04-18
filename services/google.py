import google.cloud.texttospeech as tts
import os

from database.models import CreationTask, RequestData
from misc.secrets import secret_info

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = secret_info.GOOGLE_SHEET.GOOGLE_AUTH_FILE_NAME


def create(rd: RequestData):
    text_input = tts.SynthesisInput(text=rd.text)
    voice_params = tts.VoiceSelectionParams(
        language_code=rd.task.voice.language,
        ssml_gender=rd.task.voice.tone,
        natural_speech_speed=rd.task.voice.speed,
        emotion=rd.task.voice.emotion,
        speaker=rd.task.voice.speaker
    )
    audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16)

    client = tts.TextToSpeechClient()
    response = client.synthesize_speech(
        input=text_input,
        voice=voice_params,
        audio_config=audio_config,
    )
    with open(f'temp/{rd.index}_part_{rd.task.audio_name}', "wb") as out:
        out.write(response.audio_content)

