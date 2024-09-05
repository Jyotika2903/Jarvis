import os
import random
import sys
import datetime
import pyttsx3
import speech_recognition as sr
import wikipedia
import webbrowser
import smtplib
import json  # To handle JSON files
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Email credentials
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

# Initialize Text-to-Speech engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[0].id)

REMINDER_FILE = "reminders.json"

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wish_me():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 16:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("Jarvis at your service. How may I help you?")

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 1000
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}\n")
    except sr.UnknownValueError:
        print("Could not understand audio. Please try again.")
        return "None"
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return "None"

    return query.lower()

def send_email(to, content):
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, to, content)
        server.close()
        speak("Email has been sent successfully.")
    except Exception as e:
        print(e)
        speak("Unable to send the email due to an error.")

def open_website(url, site_name):
    speak(f"Opening {site_name}.")
    webbrowser.open_new_tab(url)

def add_reminder(reminder_text):
    # Load existing reminders from the JSON file or create a new list
    try:
        with open(REMINDER_FILE, 'r') as file:
            reminders = json.load(file)
    except FileNotFoundError:
        reminders = []

    # Add the new reminder
    reminders.append({"reminder": reminder_text, "timestamp": str(datetime.datetime.now())})

    # Save the reminders back to the JSON file
    with open(REMINDER_FILE, 'w') as file:
        json.dump(reminders, file, indent=4)

    speak("Reminder has been added successfully.")

def read_reminders():
    try:
        with open(REMINDER_FILE, 'r') as file:
            reminders = json.load(file)
            if reminders:
                speak("Here are your reminders:")
                for reminder in reminders:
                    print(reminder["reminder"])
                    speak(reminder["reminder"])
            else:
                speak("You have no reminders.")
    except FileNotFoundError:
        speak("You have no reminders.")

def execute_tasks(query):
    if "wikipedia" in query:
        speak("Searching Wikipedia...")
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        print(results)
        speak(results)

    elif "open youtube" in query:
        open_website("https://www.youtube.com", "YouTube")

    elif "open google" in query:
        open_website("https://www.google.com", "Google")

    elif "open amazon" in query:
        open_website("https://www.amazon.com", "Amazon")

    elif "open spotify" in query:
        open_website("https://open.spotify.com", "Spotify")

    elif "the time" in query:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        print(current_time)
        speak(f"The time is {current_time}.")

    elif "send email" in query:
        speak("To whom should I send the email?")
        recipient = take_command()
        to = mail_list.get(recipient, None)
        if to:
            speak("What should I say?")
            content = take_command()
            send_email(to, content)
        else:
            speak("Recipient not found in the contact list.")

    elif "add reminder" in query:
        speak("What should I remind you about?")
        reminder_text = take_command()
        add_reminder(reminder_text)

    elif "read reminders" in query:
        read_reminders()

    elif any(keyword in query for keyword in ["quit", "exit", "stop", "goodbye"]):
        speak("Goodbye! Have a nice day.")
        sys.exit()

    else:
        speak("I'm sorry, I didn't understand that command.")

if __name__ == "__main__":
    wish_me()
    while True:
        query = take_command()
        if query != "None":
            execute_tasks(query)
