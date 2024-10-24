import google.generativeai as genai
import webbrowser
import os
import speech_recognition as sr
import pyttsx3
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout                                            
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label

locations = {
    "Library": "https://maps.app.goo.gl/AW5nvbvaaiL9CNhD8",
    "Volley Ball Court": "https://maps.app.goo.gl/i7j7cwUcLooVtZiVA",
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
            speak("Sorry, I did not understand that.")
        except sr.RequestError:
            speak("Sorry, the service is down.")
        except sr.WaitTimeoutError:
            speak("Listening timed out. Please try again.")
        return None

class BotApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.history_label = Label(size_hint_y=None, height=400)
        self.layout.add_widget(self.history_label)

        self.entry = TextInput(size_hint_y=None, height=50)
        self.layout.add_widget(self.entry)

        submit_button = Button(text='Submit', size_hint_y=None, height=50)
        submit_button.bind(on_press=self.on_submit)
        self.layout.add_widget(submit_button)

        # Start the voice command listening in a separate thread
        threading.Thread(target=self.listen_for_commands, daemon=True).start()

        return self.layout

    def on_submit(self, instance):
        query = self.entry.text
        self.entry.text = ""
        self.process_query(query)

    def process_query(self, query):
        if query.lower() == 'exit':
            App.get_running_app().stop()

        if "navigate" in query.lower():
            self.handle_navigation(query)
            return

        conversation_history.append(f"User: {query}")
        self.handle_generative_ai(query)

    def handle_navigation(self, query):
        place_name = query.lower().replace("navigate to", "").strip()
        found_location = False

        for location in locations.keys():
            if place_name in location.lower():
                webbrowser.open(locations[location])
                bot_response = f"Navigating to {location}..."
                conversation_history.append(f"Bot: {bot_response}")
                found_location = True
                break

        if not found_location:
            bot_response = f"Sorry, I couldn't find {place_name} in the campus locations."
            conversation_history.append(f"Bot: {bot_response}")

        self.update_history()

    def handle_generative_ai(self, query):
        try:
            genai.configure(api_key="AIzaSyDZsZvBBLs4h5JJJgGouEixbJjKJXewQd8")  # Replace with your API key
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
                    conversation_history.append(f"Bot: {bot_response}")
                    self.update_history()
                    speak(bot_response)
                else:
                    self.handle_ai_error()
            else:
                self.handle_ai_error()

        except Exception as e:
            print(f"Error: {str(e)}")
            conversation_history.append("Bot: Sorry, I couldn't generate a response.")
            self.update_history()

    def handle_ai_error(self):
        conversation_history.append("Bot: Sorry, I couldn't generate a response.")
        self.update_history()

    def update_history(self):
        self.history_label.text = "\n".join(conversation_history)

    def listen_for_commands(self):
        while True:
            query = recognize_voice()
            if query:
                self.process_query(query)

if __name__ == '__main__':
    BotApp().run()
