# timer.py

import schedule
import time
import threading
from datetime import datetime, timedelta

# This will be imported from your main assistant
try:
    from main_assistant import speak
except ImportError:
    def speak(msg):
        print(f"[Reminder/Alarm]: {msg}")

def set_reminder(reminder_time, message="This is your reminder!"):
    def job():
        speak(message)

    schedule.every().day.at(reminder_time).do(job)
    speak(f"Reminder set for {reminder_time}")

def set_alarm(minutes):
    def job():
        speak("⏰ Alarm ringing! Time's up!")

    schedule.every(minutes).minutes.do(job)
    speak(f"Alarm set for {minutes} minutes from now.")

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

def start_scheduler():
    thread = threading.Thread(target=run_schedule)
    thread.daemon = True
    thread.start()
