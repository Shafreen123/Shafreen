import pyttsx3 # isi ke help se reply karega
import datetime

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[1].id)# voice 1 for zeera 0 for david
engine.setProperty("rate",170)#speed of zira
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

def wish():
    hour=int(datetime.datetime.now().hour)
    if hour>=0 and hour<=12:
        speak("good morning Shaziaa")
    elif hour>12 and hour<=18:
        speak("good afternoon Shaziaa ")
    else:
        speak("good evening Shaziaa")
    speak("I  am Shafreen how can i help you Ma'am")