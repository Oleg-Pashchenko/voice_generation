import azure.cognitiveservices.speech as speechsdk

from database.models import RequestData
from misc import secrets


def create(rd: RequestData):
    speech_key = secrets.secret_info.AZURE_API_KEY
    service_region = "eastus"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.speech_synthesis_voice_name = rd.task.voice.speaker
    speech_config.speech_synthesis_ssml_gender = rd.task.voice.tone
    speech_config.speech_synthesis_natural_speech_speed = rd.task.voice.speed
    speech_config.speech_synthesis_emotion = rd.task.voice.emotion
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    result = speech_synthesizer.speak_text_async(rd.text).get()
    with open(f'temp/{rd.index}_part_{rd.task.audio_name}', "wb") as audio_file:
        audio_file.write(result.audio_data)
