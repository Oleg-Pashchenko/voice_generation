import azure.cognitiveservices.speech as speechsdk

speech_key = "8e8ef435d27e4bbc8616bccfdb58a40c"
service_region = "eastus"

speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

text = "Hello, this is a sample text to be synthesized."

result = speech_synthesizer.speak_text_async(text).get()

with open("output.wav", "wb") as audio_file:
    audio_file.write(result.audio_data)

print("Audio saved to output.wav.")
