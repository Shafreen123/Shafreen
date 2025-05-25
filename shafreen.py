import pyttsx3
import speech_recognition as sr
import os
import cv2
import subprocess
import undetected_chromedriver
from WishMe import wish
from conversation import get_nlp_response
import requests
from bs4 import BeautifulSoup
from weatherAtemperature import fetch_weather
import timer
import re
timer.start_scheduler()


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Zira voice
engine.setProperty('rate', 170)  # Speech rate for Zira


def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

# Function to capture the command via microphone
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1  # Pause threshold for silence
        r.energy_threshold = 300  # Energy threshold for voice detection
        print("Listening...")
        try:
            audio = r.listen(source, timeout=10, phrase_time_limit=15)
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
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
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

# Main function
if __name__ == "__main__":
    wish()  # Calls the wish function (assumed from WishMe module)
    while True:
        query = takecommand().lower()

        if "go to sleep" in query:
            speak("Ok ma'am, remember me any time you need!")
            break
        elif "talk to me" in query:
            speak("Yes sir, I am listening!")
            response = get_nlp_response(query)  # Pass the query for response generation
            speak(response)  # Speak out the generated response
        elif "thank you" in query:
            speak("My pleasure.")
        elif "open apache" in query:
            location = "C:\\Program Files\\NetBeans-21\\netbeans\\bin\\netbeans64.exe"
            os.startfile(location)
        elif "google" in query:
            from SearchNow import searchGoogle
            searchGoogle(query)
        elif "youtube" in query:
            from SearchNow import searchYoutube
            searchYoutube(query)
        elif "wikipedia" in query:
            from SearchNow import searchWikipedia
            searchWikipedia(query)
        elif "open notepad" in query:
            location = "C:\\Windows\\notepad.exe"
            os.startfile(location)
        elif "open command prompt" in query:
            os.system("start cmd")
        elif "mausam" in query:
            fetch_weather()  # Call the weather function from weatherAtemperature module
        elif "open camera" in query:
            print("Opening webcam")
            cap = cv2.VideoCapture(0)
            while True:
                ret, img = cap.read()
                if not ret:
                    break
                cv2.imshow('Webcam', img)
                if cv2.waitKey(50) == 27:  # Escape key to exit
                    break
            cap.release()
            cv2.destroyAllWindows()
        elif "open chrome shazia" in query:
            chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
            profile_name = "Shazia Afreen"
            profile_path = os.path.join("C:/Users", os.getenv("USERNAME"), "AppData/Local/Google/Chrome/User Data", profile_name)
            command = [chrome_path, f"--profile-directory={profile_name}"]
            subprocess.Popen(command)
            speak("Opening Chrome with the Shazia profile.")
        elif "alarm" in query:
            minutes_match = re.search(r'\b(\d+)\s*(minute|minutes)\b', query)
            if minutes_match:
                minutes = int(minutes_match.group(1))
                timer.set_alarm(minutes)
            else:
                speak("Please say how many minutes from now you'd like to set the alarm.")
