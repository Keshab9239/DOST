import os
import json
import threading
import urllib.request
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window

MODEL = "gemini-3.5-flash-lite"

class DostApp(App):
    def build(self):
        self.history = []
        self.memory_file = os.path.join(self.user_data_dir, "memory.json")
        self.key_file = os.path.join(self.user_data_dir, "key.json")

        root = BoxLayout(orientation="vertical", padding=12, spacing=10)

        title = Label(text="[b]DOST AI[/b]\nYour Personal Assistant",
                      markup=True, font_size=25, size_hint_y=.13)
        root.add_widget(title)

        self.api_key = TextInput(
            hint_text="Enter Gemini API Key",
            password=True, multiline=False, size_hint_y=.09
        )
        root.add_widget(self.api_key)

        self.chat = TextInput(
            text="Namaste! Main DOST hoon. Mujhse kuch bhi pucho.",
            readonly=True, multiline=True
        )
        root.add_widget(self.chat)

        self.message = TextInput(
            hint_text="Yahan apna message likho...",
            multiline=False, size_hint_y=.12
        )
        root.add_widget(self.message)

        send = Button(text="SEND", size_hint_y=.12)
        send.bind(on_press=self.send_message)
        root.add_widget(send)

        return root

    def send_message(self, instance):
        question = self.message.text.strip()
        key = self.api_key.text.strip()

        if not key:
            self.chat.text += "\n\nDOST: Pehle Gemini API key enter karo."
            return

        if not question:
            return

        self.message.text = ""
        self.chat.text += "\n\nYOU: " + question + "\nDOST: Soch raha hoon..."
        threading.Thread(
            target=self.ask_ai, args=(question, key), daemon=True
        ).start()

    def ask_ai(self, question, key):
        self.history.append({
            "role": "user",
            "parts": [{"text": question}]
        })

        data = {
            "system_instruction": {
                "parts": [{"text":
                    "Tum DOST ho, ek friendly personal AI assistant. "
                    "User se simple Hindi mein baat karo. Jawab useful rakho."
                }]
            },
            "contents": self.history[-20:]
        }

        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            + MODEL + ":generateContent"
        )

        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode(),
                headers={
                    "Content-Type": "application/json",
                    "x-goog-api-key": key
                },
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=60) as response:
                result = json.loads(response.read())

            answer = result["candidates"][0]["content"]["parts"][0]["text"]
            self.history.append({
                "role": "model",
                "parts": [{"text": answer}]
            })
            Clock.schedule_once(
                lambda dt: self.show_answer(answer)
            )

        except Exception as error:
            Clock.schedule_once(
                lambda dt: self.show_answer("Error: " + str(error))
            )

    def show_answer(self, answer):
        self.chat.text += "\n" + answer

DostApp().run()
