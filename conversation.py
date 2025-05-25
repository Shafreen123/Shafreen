import pyttsx3
import speech_recognition as sr
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY", "YOUR_API_KEY")   #mine is private


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 170)

def speak(audio):
    engine.say(audio)
    print(f"Assistant: {audio}")
    engine.runAndWait()


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        r.energy_threshold = 300
        print("Listening...")
        try:
            audio = r.listen(source, timeout=10, phrase_time_limit=15)
        except sr.WaitTimeoutError:
            speak("Listening timed out. Please try again.")
            return "none"
        except sr.RequestError as e:
            speak(f"Recognition service error: {e}")
            return "none"
        except sr.UnknownValueError:
            speak("I didn't catch that. Please speak clearly.")
            return "none"
        except Exception as e:
            speak(f"An error occurred: {e}")
            return "none"

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}")
    except sr.UnknownValueError:
        speak("Sorry, I did not understand that.")
        return "none"
    except sr.RequestError as e:
        speak(f"Could not connect to Google: {e}")
        return "none"
    except Exception as e:
        speak(f"An error occurred while recognizing: {e}")
        return "none"

    return query.lower()


def get_nlp_response(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Sorry, I couldn't generate a response: {e}"


def main():
    speak("Hello! How can I assist you today?")
    while True:
        command = take_command()
        if command == "none":
            continue

        if "exit" in command or "stop" in command:
            speak("Goodbye! Have a great day!")
            break

        response = get_nlp_response(command)
        speak(response)


if __name__ == "__main__":
    main()
