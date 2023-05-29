from Bard import Chatbot
from playsound import playsound
import speech_recognition as sr
from os import system
import whisper
import warnings
import sys

token = 'WAgV0z5Lqzna_3QZ6-K-2M_tJsrJVk6HtApmv3Wjf7bb-4QqTkJhQrCgIYnlgE1ZgCXQvQ.'
chatbot = Chatbot(token)
r = sr.Recognizer()

tiny_model = whisper.load_model('tiny')
base_model = whisper.load_model('base')
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

if sys.platform != 'darwin':
    import pyttsx3
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate, rate-50')

def prompt_Jerry(prompt):
    response = chatbot.ask(prompt)
    return response['content']

def speak(text):
    if sys.platform == 'darwin':
        ALLOWED_CHARS = set ("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,?!-_$: ")
        clean_text = ''.join(c for c in text if c in ALLOWED_CHARS)
        system(f"say '{clean_text}'")
    else:
        engine.say(text)
        engine.runAndWait()

def main():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        while True:
            try:
                playsound('wake_detected.mp3')
                print("\nPlease speak your prompt to Jerry.")
                audio = r.listen(source)
                with open("prompt.wav", "wb") as f:
                    f.write(audio.get_wav_data())
                result = base_model.transcribe('prompt.wav')
                prompt_text = result['text']
                print("\nRock:", prompt_text, '\n')
                if len(prompt_text.strip()) == 0:
                    print("Empty prompt. Please speak again.")
                    speak("Empty prompt. Please speak again.")
                    continue
            except Exception as e:
                print("Error transcribing audio: ", e)
                continue
            response = prompt_Jerry(prompt_text)
            if sys.platform.startswith('win'):
                print('Jerry response: ', response)
            else:
                print("\033[31m"+'Jerry response: ', response, '\n' + "\033[0m")
            speak(response)

main()