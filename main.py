import speech_recognition as sr 
import gtts
from playsound import playsound
import os
import time
from notion import NotionClient
from datetime import datetime

r = sr.Recognizer()

token = 'secret_2lvvGAyOL4Mh5DjM58dKE7AjTEJfqN7pwubjRBVkyB6'
database_id = '925be2b47d324e42a7e2aff0de7ce96f'


client = NotionClient(token, database_id)

ACTIVATION_COMMAND = 'hey dog'

def get_audio():
    with sr.Microphone() as source:
        print('say something')
        audio = r.listen(source)

    return audio

def audio_to_text(audio):
    text = ''
    try:
        text = r.recognize_google(audio)
    except sr.UnknownValueError:
        print('speech recognition could not understand audio')
    except sr.RequestError:
        print('could not request results from api')
    return text


def play_sound(text):
    try:
        tts = gtts.gTTS(text)
        tempfile = "temp.mp3"
        tts.save(tempfile)
        playsound(tempfile)
        os.remove(tempfile)
    except AssertionError:
        print('could not play the sound')
    






if __name__=='__main__':
    while True:
        a = get_audio()
        command = audio_to_text(a)

        if ACTIVATION_COMMAND in command.lower():
            print('activate')
            play_sound('what can i do for you')

            note = get_audio()
            note = audio_to_text(note)

            if note:
                play_sound(note)

                now = datetime.now().astimezone().isoformat()
                res = client.create_page(note, now, status='Active')
                if res.status_code == 200:
                    play_sound('stored new item')


    
