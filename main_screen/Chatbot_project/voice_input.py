import sys
import speech_recognition as sr
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import google.generativeai as genai

# Gemini API Setup
API_KEY = "AIzaSyAg_h2eXPZ9fweAf2cmwCJls0amsEV5PLc"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash-lite')

def load_data():
    try:
        with open('university_data.txt', 'r') as file:
            return file.read()
    except FileNotFoundError:
        return "Error: university_data.txt not found. Please create it."

data = load_data()

def get_gemini_response(user_query):
    system_prompt = f"""
    You are a helpful university assistant for My University. Respond only to university-related queries in natural language. 
    Use English or Roman Urdu (not native Urdu script). Be polite and natural, like a human helper.
    Use this data to answer: {data}
    If the query is not related to university info, say "Sorry, I can only help with university questions."
    Keep responses short and direct—no deep reasoning or extra analysis.
    """
    full_prompt = f"{system_prompt}\nUser: {user_query}"
    try:
        response = model.generate_content(full_prompt)
        return response.text if response.text else "No response generated."
    except Exception as e:
        return f"Error generating response: {str(e)}"

# Thread for Voice Recognition
class VoiceThread(QThread):
    recognized = pyqtSignal(str)   # emit recognized text

    def run(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                query = recognizer.recognize_google(audio, language="en-US")  # Roman format
                self.recognized.emit(query)
            except sr.WaitTimeoutError:
                self.recognized.emit("⌛ Listening timed out.")
            except sr.UnknownValueError:
                self.recognized.emit("❌ Could not understand audio.")
            except sr.RequestError:
                self.recognized.emit("⚠️ Speech Recognition service error.")

# PyQt5 App
class UniversityApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("University Chatbot App")
        self.setGeometry(100, 100, 600, 400)

        tabs = QTabWidget()
        self.setCentralWidget(tabs)

        # Screen 1: Chatbot
        chatbot_tab = QWidget()
        layout = QVBoxLayout()
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)

        self.input_field = QLineEdit()
        self.input_field.returnPressed.connect(self.send_message)
        layout.addWidget(self.input_field)

        # Send Button
        send_button = QPushButton("Send")
        send_button.clicked.connect(self.send_message)
        layout.addWidget(send_button)

        # 🎤 Voice Button
        voice_button = QPushButton("🎤 Voice Input")
        voice_button.clicked.connect(self.listen_voice)
        layout.addWidget(voice_button)

        chatbot_tab.setLayout(layout)
        tabs.addTab(chatbot_tab, "Chatbot")

        # Notifications
        notifications_tab = QWidget()
        notif_layout = QVBoxLayout()
        notif_label = QLabel("Notifications:\n- Exam on 15-Oct\n- Holiday on 20-Oct\n(Add more later)")
        notif_layout.addWidget(notif_label)
        notifications_tab.setLayout(notif_layout)
        tabs.addTab(notifications_tab, "Notifications")

    def send_message(self, text=None):
        user_query = text if text else self.input_field.text().strip()
        if user_query:
            self.chat_display.append(f"You: {user_query}")
            response = get_gemini_response(user_query)
            self.chat_display.append(f"Bot: {response}")
            self.input_field.clear()
            self.chat_display.verticalScrollBar().setValue(
                self.chat_display.verticalScrollBar().maximum()
            )

    def listen_voice(self):
        """Mic se query lene ka function (Threaded)"""
        self.chat_display.append("🎤 Listening... Speak now.")
        self.voice_thread = VoiceThread()
        self.voice_thread.recognized.connect(self.handle_voice_result)
        self.voice_thread.start()

    def handle_voice_result(self, result):
        if result.startswith("⌛") or result.startswith("❌") or result.startswith("⚠️"):
            self.chat_display.append(result)
        else:
            self.send_message(result)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UniversityApp()
    window.show()
    sys.exit(app.exec_())