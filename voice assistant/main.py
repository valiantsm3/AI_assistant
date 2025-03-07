import pyttsx3
import speech_recognition as sr
import pywhatkit
import datetime
from plyer import notification
import pyautogui
import wikipedia 
import webbrowser
from huggingchat_api import chat_with_huggingchat
from gemini_chat import chat_with_gemini
from weather_api import get_weather
from whatsapp import sendMessage


engine = pyttsx3.init()
"""VOICE"""
voices = engine.getProperty('voices')       #getting details of current voice
engine.setProperty('voice', voices[1].id)
engine.setProperty("rate",160)

def speak(audio):
    print("Assistant:", audio)
    engine.say(audio)
    engine.runAndWait()


#to giving command function
def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.2)
        while True:  # Keep asking until valid input
            print("Listening...")
            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=5)
                content = r.recognize_google(audio, language='en-in')
                print("You said:", content)
                return content.lower().strip()  # ✅ Ensures no NoneType error
            except sr.UnknownValueError:
                speak("I didn't hear that, please say again.")
            except sr.RequestError:
                speak("Check your internet connection.")
                return ""  # Avoid crash, return empty string
            except sr.WaitTimeoutError:
                print("Listening timed out, reactivating...")
                continue  # ✅ Automatically reactivates instead of crashing

#to playing music from the youtube
def play_music_on_youtube(song):
    speak(f"Playing {song} on YouTube")
    url = pywhatkit.playonyt(song, open_video=False)  # Get URL without opening
    webbrowser.open(url)  # Manually open the URL

def main_process():
    speak("Voice assistant activated.")
    while True:
        request = command()
        if not request:  # If empty, it automatically re-prompts
            continue

        #for greeting 
        elif "hello" in request:
            speak("Welcome, how can I help you, sir?")
        
        #for playing music
        elif "play music" in request:
            speak("Which song would you like to play?")
            song_name = command()
            if song_name != "":
                play_music_on_youtube(song_name)
            else:
                speak("I didn't catch the song name. Please try again.")
        
        #for date and time 
        elif "current time" in request:
            now_time=datetime.datetime.now().strftime("%H:%M")
            speak("current time is" + str(now_time))
            print(now_time)

        elif "current date" in request:
            now_date=datetime.datetime.now().strftime("%d:%m:%y")
            speak("current date is"+ str(now_date))
            print(now_date)
        
        elif "whatsapp" in request:
            sendMessage()

        #making todo list 
        elif "new task" in request:
            task=request.replace("new task","")
            task=task.strip()
            if task!="":
                speak("adding task"+task)
                with open("todo.txt","a") as file:
                    file.write(task+"\n")
        elif "daily task" in request: #to task to speak
             with open("todo.txt", "r") as file:
              task = file.read()  # Read the file content
              speak("Here are the tasks we have to do: " + task)
        elif "show work" in request:
             with open("todo.txt", "r") as file:
              tasks = file.read()
              notification.notify(
                  title="todays work",
                  message=tasks
              )
        
        #to open youtube
        elif "open youtube" in request:
            webbrowser.open("www.youtube.com")

        #to open linkedin
        elif "open linkedin" in request:
            webbrowser.open("www.linkedin.com")    

        #to open the application
        elif "open" in request:
            query=request.replace("open","")
            pyautogui.press("super")
            pyautogui.typewrite(query)
            pyautogui.sleep(2)
            pyautogui.press("enter")
        
        #to capture screen shot
        elif "take screenshot" in request:
            screenshot = pyautogui.screenshot()
            screenshot_path = "screenshot.png"
            screenshot.save(screenshot_path)
            speak(f"Screenshot saved as {screenshot_path}")
        
        #to search from wikipedia
        elif "wikipedia" in request:
            #request=request.replace("jarvis","")
            request=request.replace("search wikipedia","")
            print(request)
            result=wikipedia.summary(request,sentences=2)
            print(result)
            speak(result)
        
        # to search from google
        elif "search google" in request:
            request=request.replace("search google","")
            webbrowser.open(f"https://www.google.com/search?q={request}")

    
        # Chatbot functionality with huggingchat
        elif  "call" in request:
            speak("Sure! What would you like to talk about?")
            while True:
                user_input = command()
                if "exit chat" in user_input or "stop chatting" in user_input:
                    speak("Exiting chat mode.")
                    break
                response = chat_with_huggingchat(user_input)
                print("Chatbot:", response)
                speak(response)

        # **Chatbot Integration with Gemini**
        elif "talk to me" in request:
            speak("Sure! What would you like to talk about?")
            while True:
                user_input = command()
                if "exit chat" in user_input or "stop chatting" in user_input:
                    speak("Exiting chat mode.")
                    break
                if user_input.strip():  # Ensure input is not empty
                    response = chat_with_gemini(user_input)
                    print("Chatbot:", response)
                    speak(response)
                else:
                    speak("I couldn't hear you. Please say that again.")

     #for the wheater
        elif "weather" in request or "temperature" in request:
            speak("Which city do you want the weather for?")
            city = command()
            if city:
              weather_report = get_weather(city)
              print(weather_report)  # Print respon vs
              
              speak(weather_report)
        
        #for exit or quit 
        elif "exit" in request or "quit" in request:
            speak("Goodbye! thank you for using")
            break
        else:
            speak("I didn't get that. Please try again.")

if __name__ == "__main__":
    main_process()