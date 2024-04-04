import json
import time
import wave
import numpy as np
from google.protobuf.json_format import MessageToDict
from sic_framework.devices import Pepper
from sic_framework.devices.nao import NaoqiTextToSpeechRequest
from sic_framework.core.message_python2 import AudioMessage, AudioRequest
from sic_framework.services.dialogflow.dialogflow import DialogflowConf, GetIntentRequest, RecognitionResult, QueryResult, Dialogflow
from sic_framework.devices.common_naoqi.naoqi_motion import NaoPostureRequest, NaoqiAnimationRequest

# Constants
MUSIC_PATH = 'music-short/'
DEFAULT_SONG = 'safe-and-sound.wav'
IP_ADDRESS = '192.168.1.109'
DIALOGFLOW_KEYFILE = "dialogflow-mood-music-agent.json"

# Mapping from moods to music files
MOOD_MUSIC_MAP = {
        "happy": "shake-it-off.wav",
        "excited": "cant-hold-us.wav",
        "sexy": "sexy-and-i-know-it.wav",
        "party": "give-me-everything.wav",
        "bootylicious": "starships.wav",
        "sad": "demons.wav",
        "stressed": "riptide.wav",
        "spanish": "despacito.wav",
        "neutral": "safe-and-sound.wav",
        "nostalgic": "secrets.wav",
        "unwell": "viva-la-vida.wav",
        "pumped": "pump-it.wav",
        "angry": "renegades.wav",
    }

MOOD_RESPONSES = {
        "happy": "It's wonderful to see you happy! Let's play some cheerful music!",
        "excited": "I can feel your excitement! Time for a track to match that energy.",
        "sexy": "Feeling confident, I see! Here's a tune to walk that walk.",
        "party": "Who's in the mood for a party? Let's go, nothing can hold us!",
        "bootylicious": "Let's turn up the beat and get moving! Music coming right up.",
        "sad": "I'm here for you. Let's play some soft uplifting music to brighten your day.",
        "stressed": "Let's take a moment to relax. I'll play some calm music for you.",
        "neutral": "Feeling so-so? Let's see if we can gently lift that mood with some tunes.",
        "nostalgic": "Nostalgic, aren't we? Let's revisit some memories with this track.",
        "spanish": "Ready for some fiery Spanish beats? Let's dance!",
        "unwell": "I hope you feel better soon. Here's some gentle music to comfort you.",
        "pumped": "Ready to conquer the world? Here's a powerful track to fuel your fire!",
        "angry": "I sense some tension. Let's play something to help soothe and relax you."
    }

def play_music(file_path):
    print("Trying to play music")
    try:
        wavefile = wave.open(file_path, 'rb')
    except IOError:
        print(f"Failed to open file {file_path}")
        return

    samplerate = wavefile.getframerate()
    print("Playing audio file:")
    print("  File:", file_path)
    print("  Sample rate:", samplerate)
    print("  Length:", wavefile.getnframes())

    sound = wavefile.readframes(wavefile.getnframes())
    message = AudioMessage(sample_rate=samplerate*2, waveform=sound)  # Adjust sample_rate if needed
    pepper.speaker.send_message(message)

    print("Audio sent, without waiting for it to complete playing.")

# Example callback function for handling different moods
def handle_mood(mood):
    music_file_path = f"{MUSIC_PATH}{MOOD_MUSIC_MAP.get(mood.lower(), DEFAULT_SONG)}"
    response_text = MOOD_RESPONSES.get(mood.lower(), "Let's enjoy some music together!")
    return response_text, music_file_path

# the callback function
def on_dialog(message):
    if message.response and message.response.recognition_result.is_final:
        print("Transcript:", message.response.recognition_result.transcript)
        
# connect to the robot
pepper = Pepper(ip=IP_ADDRESS)

# load the key json file
keyfile_json = json.load(open(DIALOGFLOW_KEYFILE))

# set up the config
conf = DialogflowConf(keyfile_json=keyfile_json, sample_rate_hertz=16000)

# initiate Dialogflow object
dialogflow = Dialogflow(ip='localhost', conf=conf)

# connect the output of NaoqiMicrophone as the input of DialogflowComponent
dialogflow.connect(pepper.mic)

# register a callback function to act upon arrival of recognition_result
dialogflow.register_callback(on_dialog)

# DEMO START
pepper.motion.request(NaoPostureRequest("Stand", .5))
time.sleep(1)
#pepper.motion.request(NaoqiAnimationRequest("Hey_3"), block=True)
pepper.tts.request(NaoqiTextToSpeechRequest("Hello, I'm Pepper. What is your name?"))
#time.sleep(1)
#reply = pepper.motion.request(NaoPostureRequest("Stand", .5))
print(" -- Ready -- ")
x = np.random.randint(10000)

try:
    for i in range(25):
        print(" ----- Conversation turn", i)
        reply = dialogflow.request(GetIntentRequest(x))

        print("Intent:", reply.intent)
        print("Raw result:", reply.rawresult)

        mood = reply.mood
        print("Mood: ", mood)

        if mood:    
            response_text, music_file_path = handle_mood(mood)
            print("Response:", response_text)
            pepper.tts.request(NaoqiTextToSpeechRequest(response_text))
            # Play the selected music
            play_music(music_file_path)
            time.sleep(25)
            mood = None
        
        if reply.fulfillment_message:
            text = reply.fulfillment_message
            print("Reply:", text)
            pepper.tts.request(NaoqiTextToSpeechRequest(text))
except KeyboardInterrupt:
    print("Stop the dialogflow component.")
    dialogflow.stop()
