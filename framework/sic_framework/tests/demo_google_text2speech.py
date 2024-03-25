from sic_framework.core.message_python2 import AudioMessage, AudioRequest
from sic_framework.devices import Nao
from sic_framework.devices.common_desktop.desktop_speakers import SpeakersConf
from sic_framework.devices.desktop import Desktop
from sic_framework.services.text2speech.text2speech_service import Text2Speech, Text2SpeechConf, GetSpeechRequest, SpeechResult


"""
Google Text2Speech service should be running. You can start it with:
[services/text2speech] python text2speech_service.py 

NOTE: you need to have setup Cloud Text-to-Speech API in your Google Cloud Console and configure the credential keyfile.
See https://console.cloud.google.com/apis/api/texttospeech.googleapis.com/ 
"""

# nao = Nao("192.168.0.191")

tts_conf = Text2SpeechConf(keyfile="your_keyfile.json")
tts = Text2Speech(conf=tts_conf)
reply = tts.request(GetSpeechRequest("Hello, how are you?"))

comp = Desktop(speakers_conf=SpeakersConf(sample_rate=reply.sample_rate))
comp.speakers.request(AudioRequest(reply.waveform, reply.sample_rate))

reply = tts.request(GetSpeechRequest(text="Hello, how are you?", voice_name="en-US-Neural2-G", ssml_gender="FEMALE"))
comp.speakers.request(AudioRequest(reply.waveform, reply.sample_rate))

reply = tts.request(GetSpeechRequest(text="Hello, how are you?", voice_name="en-US-Neural2-I", ssml_gender="MALE"))
comp.speakers.request(AudioRequest(reply.waveform, reply.sample_rate))
