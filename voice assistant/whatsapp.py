import pywhatkit
import pyttsx3
import speech_recognition as sr
from datetime import datetime

# Initialize the text-to-speech engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)  # Set voice to the first available
engine.setProperty("rate", 170)  # Set speech rate

# Function to convert text to speech
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Function to take voice input from the user
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1  # Pause threshold before processing
        r.energy_threshold = 300  # Adjust energy threshold for better recognition
        audio = r.listen(source, timeout=4)  # Listen for up to 4 seconds

    try:
        print("Understanding...")
        query = r.recognize_google(audio, language='en-in')  # Convert speech to text
        print(f"You Said: {query}\n")
    except Exception:
        print("Say that again...")
        return "None"

    return query

# Function to send a WhatsApp message
def sendMessage():
    while True:
        speak("Enter the phone number of the recipient with country code.")
        phone_number = input("Enter the phone number (with country code): ")  # Take phone number input

        if phone_number.startswith("+"):
            break
        else:
            print("Error: Country Code Missing in Phone Number!")
            speak("Country code is missing. Please enter again.")

    # Get message from user
    speak("What's the message?")
    message = input("Enter the message: ")

    try:
        now = datetime.now()
        hour = now.hour
        minute = now.minute + 1  # Ensure the message is scheduled in the next minute
        
        if minute >= 60:
            hour += 1
            minute = 0  # Reset minute to 0 if it exceeds 59

        # Send WhatsApp message
        pywhatkit.sendwhatmsg(phone_number, message, time_hour=hour, time_min=minute, wait_time=5)
        speak("Message sent successfully.")

    except Exception as e:
        print(f"Error: {e}")
        speak("An error occurred while sending the message. Please try again.")


