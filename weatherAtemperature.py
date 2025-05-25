import requests
from bs4 import BeautifulSoup
import pyttsx3# isi ke help se reply karega
import speech_recognition as sr # capture inpute from microphone
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[1].id)# voice 1 for zeera 0 for david
engine.setProperty("rate",170)#speed of zira
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        r.energy_threshold = 300
        print("Listening...")
        try:
            audio = r.listen(source, timeout=10, phrase_time_limit=15)  # Listen with increased timeout
        except sr.WaitTimeoutError:
            speak("Listening timed out while waiting for phrase to start. Please try again.")
            return "none"
        except sr.RequestError as e:
            speak(f"Could not request results; {e}")
            return "none"
        except sr.UnknownValueError:
            speak("Could not understand the audio, please speak clearly.")
            return "none"
        except Exception as e:
            speak(f"An error occurred: {e}")
            return "none"

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')  # Recognize speech
        print(f"user said: {query}")
    except sr.UnknownValueError:
        speak("Sorry, I did not get that. Please say that again.")
        return "none"
    except sr.RequestError as e:
        speak(f"Could not request results from Google Speech Recognition service; {e}")
        return "none"
    except Exception as e:
        speak(f"An error occurred during recognition: {e}")
        return "none"

    return query.lower()


def fetch_weather():
    while True:
        speak("Can you specify the location?")
        location = takecommand().lower()
        print(f"user said {location}")

        api_key = "8a64ef8cb4cdb02b19d400fdc665027d"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"

        try:
            response = requests.get(url)
            response.raise_for_status()

            data = response.json()
            temp = data['main']['temp']
            description = data['weather'][0]['description']
            speak(f"The temperature in {location} is {temp}°C with {description}.")
            break

        except requests.exceptions.HTTPError as http_err:
            speak(f"HTTP error occurred: {http_err}. Please try again.")
        except requests.exceptions.ConnectionError as conn_err:
            speak(f"Connection error occurred: {conn_err}. Please check your internet connection and try again.")
        except requests.exceptions.Timeout as timeout_err:
            speak(f"Timeout error occurred: {timeout_err}. Please try again.")
        except requests.exceptions.RequestException as req_err:
            speak(f"An error occurred: {req_err}. Please try again.")


