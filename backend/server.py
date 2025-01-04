from flask import Flask, request, jsonify
from flask_cors import CORS
from threading import Thread
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import smtplib
import speech_recognition as sr
import numpy as np
from datetime import datetime
import spotipy # type: ignore
# import json 


# Your Hot words or Wake up words.
HOT_WORDS = ["jarvis", "hello jarvis"]

# SMTP Configuration
HOST = "smtp.gmail.com"
PORT = 587

# Mail Credentials
FROM_EMAIL = "shraddhabandekar73@gmail.com"
TO_EMAIL = "gaureshkarekar777@gmail.com"
PASSWORD = "tjza bzfh vevc dibi"

# Authentication/Credentials for spotify
username = '31mpatrjour2nqkqij6erw7qsdue'
clientID = 'bf2a9f8aa61447d888f308c1469e1354'
clientSecret = '8fdb9262175844eeb6c3d4e0c6f255b2'
redirect_uri = 'http://localhost:5000/callback'
oauth_object = spotipy.SpotifyOAuth(clientID, clientSecret, redirect_uri) 
token_dict = oauth_object.get_access_token() 
token = token_dict['access_token'] 
spotifyObject = spotipy.Spotify(auth=token) 
user_name = spotifyObject.current_user() 

def listen_for_hotword():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for hot words...")
        try:
            audio = recognizer.listen(source, timeout=5)
            return recognizer.recognize_google(audio).lower()
        except sr.UnknownValueError:
            return ""
        except sr.WaitTimeoutError:
            print("Listening timed out.")
            return ""

def sendEmail(to, content):
    # Email Content
    SUBJECT = "Test Email"
    BODY = content
    MESSAGE = f"Subject: {SUBJECT}\n\n{BODY}"
    try:
        # Connect to SMTP server
        smtp = smtplib.SMTP(HOST, PORT)
        smtp.ehlo()  # Identify ourselves to the SMTP server
        smtp.starttls()  # Start TLS encryption
        smtp.ehlo()

        # Login to Gmail account
        smtp.login(FROM_EMAIL, PASSWORD)

        # Send email
        smtp.sendmail(FROM_EMAIL, TO_EMAIL, MESSAGE)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        smtp.quit()  # Terminate the SMTP session

def takeCommand():
    #It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 2
        audio = r.listen(source)
    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in') #Using google for voice recognition.
        print(f"User said: {query}\n")  #User query will be printed.
    except Exception as e:
        # print(e)    
        print("Say that again please...")   #Say that again will be printed in case of improper voice 
        return "None" #None string will be returned
    return query

def respond_to_hotword():
    print("Jarvis Activated ! How can I assist you?")
    speak("Hello I am Jarvis build on python")
    # Add your response logic here, e.g., play audio, send a request, etc.
    while 1:
        query = takeCommand().lower() #Converting user query into lower case
        print(query)
        # Logic for executing tasks based on query
        if 'wikipedia' in query:  #if wikipedia found in the query then this block will be executed
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2) 
            speak("According to Wikipedia")
            print(results)
            speak(results)
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")    
        elif 'play music' in query:
            speak('Which song would you like to listen ?')
            search_song = takeCommand().lower() #Converting user query into lower case 
            play_song(search_song)
            print('{search_song} Song has opened in your browser.')
        elif 'what is the time' in query:
            strTime = datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir, the time is {strTime}")
        elif 'stop' in query:
            break
        elif 'email' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "gaureshkarekar777@gmail.com"    
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry my friend. I am not able to send this email")
    
def detect_hotword():
    while True:
        spoken_text = listen_for_hotword()
        if any(hot_word in spoken_text for hot_word in HOT_WORDS):
            print(f"Hot word detected at {datetime.now()}: {spoken_text}")
            respond_to_hotword()
        else:
            print("No hot word detected.")

def play_song(search_song):
    results = spotifyObject.search(search_song, 1, 0, "track") 
    songs_dict = results['tracks'] 
    song_items = songs_dict['items'] 
    song = song_items[0]['external_urls']['spotify'] 
    webbrowser.open(song)

engine = pyttsx3.init('sapi5')

voices= engine.getProperty('voices') #getting details of current voice

engine.setProperty('voice', voices[1].id)
app = Flask(__name__)
CORS(app)

def speak(audio):
    def tts():
        engine = pyttsx3.init()  # Reinitialize within the thread
        engine.say(audio)
        engine.runAndWait()
    Thread(target=tts).start()  # Run TTS in a separate thread to avoid blocking

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Get JSON data from the frontend
        data = request.json
        return jsonify({"message": "Data received successfully!", "data": data})
    return "Hello, World!"

@app.route('/jarvis')
def jarvis():
    msg = 'Hello, my name is Jarvis. I am built on top of Python. How can I help you?'
    speak(msg)
    return msg

@app.route('/spotify')
def spotify():
    while True:
        print("Welcome to the project, " + user_name['display_name']) 
        print("0 - Exit the console") 
        print("1 - Search for a Song") 
        user_input = int(input("Enter Your Choice: ")) 
        if user_input == 1: 
            search_song = input("Enter the song name: ") 
            results = spotifyObject.search(search_song, 1, 0, "track") 
            songs_dict = results['tracks'] 
            song_items = songs_dict['items'] 
            song = song_items[0]['external_urls']['spotify'] 
            webbrowser.open(song) 
            print('Song has opened in your browser.') 
        elif user_input == 0: 
            print("Good Bye, Have a great day!") 
            break
        else: 
            print("Please enter valid user-input.")

@app.route('/detect')
def detect():
    try:
        detect_hotword()
    except KeyboardInterrupt:
        print("Hot word detection stopped.")


if __name__ == '__main__':
    app.run(debug=True)