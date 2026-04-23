import sys
import os
import asyncio
import threading
import pygame
import speech_recognition as sr
from langdetect import detect
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel
)
from PyQt5.QtCore import QThread, pyqtSignal
import google.generativeai as genai
import edge_tts

# ========== Gemini API Setup ==========
API_KEY = "AIzaSyAg_h2eXPZ9fweAf2cmwCJls0amsEV5PLc"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash-lite")

# ========== Load University Data ==========
def load_data():
    try:
        with open("university_data.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Error: university_data.txt not found."

data = load_data()

# ========== Detect Language ==========
def detect_language(text):
    urdu_chars = [c for c in text if "\u0600" <= c <= "\u06FF"]
    if urdu_chars:
        return "urdu"
    try:
        lang = detect(text)
        return "urdu" if lang == "ur" else "english"
    except:
        return "english"

# ========== Text-to-Speech ==========
async def generate_tts(text, output_file):
    lang = detect_language(text)
    voice = "ur-PK-AsadNeural" if lang == "urdu" else "en-US-JennyNeural"
    tts = edge_tts.Communicate(text, voice)
    await tts.save(output_file)

def play_audio(file_path):
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        print("Audio error:", e)
    finally:
        pygame.mixer.quit()
        if os.path.exists(file_path):
            os.remove(file_path)

def speak_text_threadsafe(text):
    def run():
        asyncio.run(speak_text(text))
    threading.Thread(target=run, daemon=True).start()

async def speak_text(text):
    output_file = "voice_output.mp3"
    await generate_tts(text, output_file)
    play_audio(output_file)

# ========== Urdu Transliteration Helper ==========
# Converts Roman Urdu to Urdu Script (basic mapping for common sounds)
import re

def roman_to_urdu(text):
    mapping = {
        "aap": "آپ", "ka": "کا", "kya": "کیا", "mein": "میں", "tum": "تم", "mera": "میرا",
        "kaun": "کون", "ha": "ہے", "hai": "ہے", "nahi": "نہیں", "sath": "ساتھ",
        "baat": "بات", "kar": "کر", "sakta": "سکتا", "sakti": "سکتی", "urdu": "اردو"
    }
    for eng, ur in mapping.items():
        text = re.sub(rf"\b{eng}\b", ur, text, flags=re.IGNORECASE)
    return text

# ========== Gemini Response ==========
def get_gemini_response(user_query):
    system_prompt = f"""
    You are a helpful university assistant.
    Respond only to university-related queries.
    Use the same language as user's query.
    Data: {data}
    If not related to university info, say:
    "Sorry, I can only help with university questions."
    """
    try:
        response = model.generate_content(f"{system_prompt}\nUser: {user_query}")
        return response.text if response.text else "No response."
    except Exception as e:
        return f"Error: {str(e)}"

# ========== Voice Recognition ==========
class VoiceThread(QThread):
    recognized = pyqtSignal(str)
    listening = pyqtSignal(str)

    def run(self):
        recognizer = sr.Recognizer()
        recognizer.energy_threshold = 150
        recognizer.dynamic_energy_threshold = True
        recognizer.pause_threshold = 1.2

        with sr.Microphone() as source:
            try:
                self.listening.emit("🎙 Listening... please speak clearly.")
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)
                self.listening.emit("⌛ Processing voice...")

                urdu_text, english_text = "", ""

                # Try Urdu first
                try:
                    urdu_text = recognizer.recognize_google(audio, language="ur-PK")
                except sr.UnknownValueError:
                    pass

                # Try English next
                try:
                    english_text = recognizer.recognize_google(audio, language="en-US")
                except sr.UnknownValueError:
                    pass

                # Always prefer Urdu if any Urdu-like content detected
                final_query = urdu_text if len(urdu_text) >= len(english_text) else english_text

                # --- Urdu purifier ---
                def clean_to_pure_urdu(text):
                    roman_to_urdu_map = {
                        "hai": "ہے",
                        "mera": "میرا",
                        "apka": "آپکا",
                        "ap": "آپ",
                        "kya": "کیا",
                        "kaun": "کون",
                        "ka": "کا",
                        "ki": "کی",
                        "university": "یونیورسٹی",
                        "teacher": "استاد",
                        "sir": "سر",
                        "shukriya": "شکریہ",
                        "student": "طالب علم",
                        "class": "کلاس",
                        "exam": "امتحان",
                        "holiday": "چھٹی",
                        "good": "اچھا",
                        "bad": "برا",
                        "ok": "ٹھیک",
                        "hello": "ہیلو",
                        "thanks": "شکریہ"
                    }

                    for en, ur in roman_to_urdu_map.items():
                        text = text.replace(en, ur)
                    return text

                # If Urdu text is mixed (some English words remain), clean them
                if final_query:
                    # If it contains even one Urdu character, treat as Urdu
                    if any('\u0600' <= c <= '\u06FF' for c in final_query):
                        final_query = clean_to_pure_urdu(final_query)

                if not final_query.strip():
                    final_query = "❌ Could not understand your voice."

                self.recognized.emit(final_query)

            except sr.WaitTimeoutError:
                self.recognized.emit("⌛ Listening timed out.")
            except Exception as e:
                self.recognized.emit(f"⚠️ Error: {str(e)}")

# ========== PyQt App ==========
class UniversityApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("University Chatbot")
        self.setGeometry(100, 100, 600, 400)

        tabs = QTabWidget()
        self.setCentralWidget(tabs)

        chatbot_tab = QWidget()
        layout = QVBoxLayout()
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)

        self.input_field = QLineEdit()
        self.input_field.returnPressed.connect(self.send_message)
        layout.addWidget(self.input_field)

        send_button = QPushButton("Send")
        send_button.clicked.connect(self.send_message)
        layout.addWidget(send_button)

        voice_button = QPushButton("Voice Input")
        voice_button.clicked.connect(self.listen_voice)
        layout.addWidget(voice_button)

        chatbot_tab.setLayout(layout)
        tabs.addTab(chatbot_tab, "Chatbot")

        notifications_tab = QWidget()
        notif_layout = QVBoxLayout()
        notif_label = QLabel("Notifications:\n- Exam: 15 Oct\n- Holiday: 20 Oct")
        notif_layout.addWidget(notif_label)
        notifications_tab.setLayout(notif_layout)
        tabs.addTab(notifications_tab, "Notifications")

    def send_message(self, text=None):
        user_query = text if text else self.input_field.text().strip()
        if user_query:
            self.chat_display.append(f"You: {user_query}")
            response = get_gemini_response(user_query)
            self.chat_display.append(f"Bot: {response}")
            speak_text_threadsafe(response)
            self.input_field.clear()
            self.chat_display.verticalScrollBar().setValue(
                self.chat_display.verticalScrollBar().maximum()
            )

    def listen_voice(self):
        self.voice_thread = VoiceThread()
        self.voice_thread.listening.connect(lambda msg: self.chat_display.append(msg))
        self.voice_thread.recognized.connect(self.handle_voice_result)
        self.voice_thread.start()

    def handle_voice_result(self, result):
        if result.startswith(("⌛", "❌", "⚠️")):
            self.chat_display.append(result)
        else:
            self.chat_display.append(f"🎧 Recognized: {result}")
            self.send_message(result)


# ========== Run ==========
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UniversityApp()
    window.show()
    sys.exit(app.exec_())
