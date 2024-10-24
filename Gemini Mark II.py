import google.generativeai as genai
import sys
import tkinter as tk
from tkinter import messagebox
import webbrowser
import os
import pyautogui
import speech_recognition as sr
import pyttsx3
import threading
from PIL import ImageGrab
import pytesseract
import time

instalink = "https://www.instagram.com/srmistup/?hl=en"
xlink = "https://x.com/i/flow/login?redirect_after_login=%2Fsrmup"
mainweblink = "https://www.srmup.in/"
stplink = "https://sp.srmist.edu.in/srmiststudentportal/students/loginManager/youLogin.jsp"
connlink = "https://connect-srm.vercel.app/"

locations = {
    "Library": "https://maps.app.goo.gl/AW5nvbvaaiL9CNhD8",
    "VolleyBall Court": "https://maps.app.goo.gl/i7j7cwUcLooVtZiVA",
    "Main Building": "https://maps.app.goo.gl/gHzyhpKhfkv159yx9",
    "Mechanical Workshop": "https://maps.app.goo.gl/MeFVwzJRQq2FRNAu5",
    "Electrical Department": "https://maps.app.goo.gl/5qu4XjKhuy9Dmz789",
    "ATM": "https://maps.app.goo.gl/y4o4KEpawUEd2RwG8",
    "Hostel": "https://maps.app.goo.gl/PMbpHb76udsx2joA6",
    "Main Gate": "https://maps.app.goo.gl/GnswUrHKgJC8oywV7", 
    "Pharmacy Gate": "https://maps.app.goo.gl/iUMdjSyyYjn5UhoQ9"
}

conversation_history = []
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

HEAD_COLOR = "#0c0536"  
BACKGROUND_COLOR = "#0c0536"  
FONT_COLOR = "#FFA500"  
FOREGROUND_COLOR = "#222224"

FONT_NAME = "Arial"  
FONT_SIZE = 12 

voices = tts_engine.getProperty('voices')
tts_engine.setProperty('voice', voices[0].id)

def type_message(message):
    pyautogui.typewrite(message, interval=0.2)

def rgn():
    if len(conversation_history) >= 2:
        last_query = conversation_history[-2].split("User: ", 1)[-1]
        entry.delete(0, tk.END)
        entry.insert(0, last_query)
        on_submit()

def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

def recognize_voice():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  
        audio = recognizer.listen(source, timeout=7)  
        try:
            query = recognizer.recognize_google(audio)
            print(f"You said: {query}")
            return query
        except sr.UnknownValueError:
            print("Waiting for response or Bad Response, please try again!")
        except sr.RequestError:
            speak("Sorry, the service is down.")
        except sr.WaitTimeoutError:
            speak("Listening timed out. Please try again.")
        return None
    
def on_submit(query=None):
    if query is None:
        query = entry.get()

    if query.lower() == 'exit' or query.lower() == 'good bye':
        root.destroy()
        sys.exit()
    if "mark calculator" in query.lower() or "marks calculator" in query.lower():
        os.startfile("D:\\Coding\\Python\\Gemini AI APP\\GPAC.py")
        bot_response = "Opening CGPA Calculator, Sir!"
        display_bot_response(bot_response)
        return
    if "image search" in query.lower():
        webbrowser.open("lens.google.com")
        time.sleep(3)
        pyautogui.hotkey('ctrl', 'v')
        return
    
    if "feedback" in query.lower():
        os.startfile("D:\\Coding\\Python\\Gemini AI APP\\feedback.py")
        bot_response = "Opening the feedback form"
        display_bot_response(bot_response)
        return
    if "college instagram" in query.lower():
        webbrowser.open(instalink)
        bot_response = "Opening College Instagram Page, Sir"
        display_bot_response(bot_response)
        return 
    if "college twitter" in query.lower():
        webbrowser.open(xlink)
        bot_response = "Opening College Twitter Page, Sir"
        display_bot_response(bot_response)
        return 
    if "main website" in query.lower():
        webbrowser.open(mainweblink)
        bot_response = "Opening College web page, Sir"
        display_bot_response(bot_response)
        return 
    if "student portal" in query.lower():
        webbrowser.open(stplink)
        bot_response = "Opening Student Portal, Sir"
        display_bot_response(bot_response)
        return 
    if "connect portal" in query.lower():
        webbrowser.open(connlink)
        bot_response = "Opening SRM Connect Portal, Sir"
        display_bot_response(bot_response)
        return 
    if "vs code" in query.lower() or "code editor" in query.lower():
        os.startfile("C:\\Users\\chauh\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Visual Studio Code\\Visual Studio Code.lnk")
        bot_response = "Opening Code Editor, Sir."
        display_bot_response(bot_response)
        return
    if query.lower().startswith('search youtube for '):
        search_query = query[14:]
        search_url = f"https://www.youtube.com/results?search_query={search_query.replace(' ', '+')}"
        webbrowser.open(search_url)
        bot_response = f"Searching YouTube for: {search_query}"
        display_bot_response(bot_response)
        return
    if "speed test" in query.lower():
        webbrowser.open("https://speedtest.net/run#")
        bot_response = "Opening Speed Test, Sir."
        display_bot_response(bot_response)
        return
    if "google" in query.lower():
        search_query = query[query.lower().index("google") + 6:].strip()
        url = f"https://www.google.com/search?q={search_query}"
        bot_response = "Googling Your Query."
        display_bot_response(bot_response)
        webbrowser.open(url)
        return 
    if "notes" in query.lower():
        os.startfile("D:\\Coding\\Python\\Gemini AI APP\\notes.py")
        bot_response = "Opening the Vast Note Collection, Sir."
        display_bot_response(bot_response)
        return
    if "club" in query.lower():
        webbrowser.open("https://www.srmup.in/cpage.aspx?mpgid=6&pgidtrail=44")
        bot_response = "Opening the Detailed Club list."
        display_bot_response(bot_response)
        return

    if "navigate" in query.lower():
        place_name = query.lower().replace("navigate to", "").strip()
        found_location = False
        for location in locations.keys():
            if place_name in location.lower():
                bot_response = f"Navigating to {location}..."
                display_bot_response(bot_response)
                webbrowser.open(locations[location])
                found_location = True
                break
        if not found_location:
            bot_response = f"Sorry, I couldn't find {place_name} in the campus locations."
            display_bot_response(bot_response)
        return

    conversation_history.append(f"User: {query}") 

    try:
        genai.configure(api_key="Add your own API Key")
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 40,
            "max_output_tokens": 150
        }
        model = genai.GenerativeModel("gemini-pro", generation_config=generation_config)
        conversation_input = "\n".join(conversation_history)
        response = model.generate_content([conversation_input])
        
        if response.candidates and hasattr(response.candidates[0], 'content'):
            content = response.candidates[0].content
            if hasattr(content, 'parts') and content.parts:
                bot_response = content.parts[0].text
                if not conversation_history or conversation_history[-1] != f"Bot: {bot_response}":
                    conversation_history.append(f"Bot: {bot_response}")
                if "code" in query.lower() or "script" in query.lower():
                    display_bot_response(bot_response, speak_text=False)
                else:
                    display_bot_response(bot_response, speak_text=True)
            else:
                bot_response = "Sorry, I couldn't generate a response. Please try again."
                conversation_history.append(f"Bot: {bot_response}")
                display_bot_response(bot_response)
        else:
            bot_response = "Sorry, I couldn't generate a response. Please try again."
            conversation_history.append(f"Bot: {bot_response}")
            display_bot_response(bot_response)
    except Exception as e:
        print(f"Error: {str(e)}")
        bot_response = "An error occurred while processing your request."
        conversation_history.append(f"Bot: {bot_response}")
        display_bot_response(bot_response)

def display_bot_response(response, speak_text=True):
    bot_text.delete(1.0, tk.END)
    bot_text.insert(tk.END, response)
    bot_text.see(tk.END)
    if speak_text:
        speak(response)

def start_voice_recognition():
    while True:
        command = recognize_voice()
        if command:
            print(f"Voice command recognized: {command}")
            on_submit(command)

def start_voice_recognition_thread():
    thread = threading.Thread(target=start_voice_recognition, daemon=True)
    thread.start()

root = tk.Tk()
root.title("Gemini AI App")
root.geometry("800x600")

root.configure(bg=BACKGROUND_COLOR)

entry = tk.Entry(root, width=70, bg=FOREGROUND_COLOR, fg=FONT_COLOR, font=(FONT_NAME, FONT_SIZE))
entry.pack(pady=10)

submit_button = tk.Button(root, text="Submit", command=on_submit, bg=HEAD_COLOR, fg=FONT_COLOR, font=('Comic Sans', '20'))
submit_button.pack(pady=5)

bot_text = tk.Text(root, wrap=tk.WORD, bg=FOREGROUND_COLOR, fg=FONT_COLOR, font=(FONT_NAME, FONT_SIZE))
bot_text.pack(pady=10)

start_voice_recognition_thread()
root.mainloop()
