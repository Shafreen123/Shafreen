import webbrowser
import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia

# Initialize the speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Use voice 1 for Zeera, 0 for David
engine.setProperty("rate", 170)

def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1  # Duration of silence considered as a pause in speech
        r.energy_threshold = 300  # Minimum level of audio energy to consider for voice detection
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

def searchGoogle(query):
    if "google" in query:
        query = query.replace("shafreen", "").replace("google search", "").replace("google", "")
        speak("Searching on Google...")
        try:
            pywhatkit.search(query)
            result = wikipedia.summary(query, sentences=2)
            speak(result)
        except wikipedia.DisambiguationError as e:
            speak("The query resulted in multiple results. Please be more specific.")
        except Exception as e:
            speak(f"An error occurred: {e}")
            speak("Not able to find the desired outcome")

def searchYoutube(query):
    if "youtube" in query:
        speak("Searching on YouTube...")
        query = query.replace("shafreen", "").replace("youtube search", "").replace("youtube", "")
        web = "https://www.youtube.com/results?search_query=" + query
        webbrowser.open(web)
        try:
            pywhatkit.playonyt(query)
            speak("Playing on YouTube")
        except Exception as e:
            speak(f"An error occurred: {e}")

def searchWikipedia(query):
    if "wikipedia" in query:
        speak("Searching on Wikipedia...")
        query = query.replace("shafreen", "").replace("wikipedia search", "").replace("wikipedia", "")
        try:
            results = wikipedia.summary(query, sentences=5)
            speak("According to Wikipedia")
            print(results)
            speak(results)
        except wikipedia.DisambiguationError as e:
            speak("The query resulted in multiple results. Please be more specific.")
        except Exception as e:
            speak(f"An error occurred: {e}")


