import azure.cognitiveservices.speech as speechsdk


def create(task):
    speech_key = "8e8ef435d27e4bbc8616bccfdb58a40c"
    service_region = "eastus"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    result = speech_synthesizer.speak_text_async(task.text).get()
    with open("output.wav", "wb") as audio_file:
        audio_file.write(result.audio_data)

