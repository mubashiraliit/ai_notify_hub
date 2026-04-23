import sys
import speech_recognition as sr
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import google.generativeai as genai

# === Gemini API Setup ===
API_KEY = "AIzaSyAg_h2eXPZ9fweAf2cmwCJls0amsEV5PLc"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash-lite')

# === Load University Data ===
def load_data():
    try:
        with open('university_data.txt', 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return "Error: university_data.txt not found."

data = load_data()

# === Gemini Response Function ===
def get_gemini_response(user_query):
    system_prompt = f"""
    You are a helpful university assistant for My University.
    Respond only to university-related queries in natural language.
    Reply in the same language (English or Roman Urdu) as the user's query.
    Be polite, short, and clear — no deep reasoning.
    Use this data to answer: {data}
    If irrelevant, reply: "Sorry, I can only help with university questions."
    """
    full_prompt = f"{system_prompt}\nUser: {user_query}"
    try:
        response = model.generate_content(full_prompt)
        return response.text or "No response generated."
    except Exception as e:
        return f"Error: {e}"

# === Background Voice Thread ===
class VoiceThread(QThread):
    recognized = pyqtSignal(str)

    def run(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.pause_threshold = 2.3      # Seconds of silence before stopping
            recognizer.energy_threshold = 300     # Adjust mic sensitivity
            recognizer.dynamic_energy_threshold = True
            try:
                audio = recognizer.listen(source, timeout=8, phrase_time_limit=15)
                text = recognizer.recognize_google(audio, language="en-US")
                self.recognized.emit(text)
            except sr.WaitTimeoutError:
                self.recognized.emit("⌛ Listening timed out.")
            except sr.UnknownValueError:
                self.recognized.emit("❌ Could not understand audio.")
            except sr.RequestError:
                self.recognized.emit("⚠️ Network error with recognition service.")

# === Main App ===
class UniversityApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("University Chatbot App")
        self.setGeometry(100, 100, 600, 400)

        tabs = QTabWidget()
        self.setCentralWidget(tabs)

        # --- Chatbot Tab ---
        chatbot_tab = QWidget()
        layout = QVBoxLayout()

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)

        self.input_field = QLineEdit()
        self.input_field.returnPressed.connect(self.send_message)
        layout.addWidget(self.input_field)

        send_btn = QPushButton("Send")
        send_btn.clicked.connect(self.send_message)
        layout.addWidget(send_btn)

        voice_btn = QPushButton("🎤 Voice Input")
        voice_btn.clicked.connect(self.listen_voice)
        layout.addWidget(voice_btn)

        chatbot_tab.setLayout(layout)
        tabs.addTab(chatbot_tab, "Chatbot")

        # --- Notifications Tab ---
        notif_tab = QWidget()
        notif_layout = QVBoxLayout()
        notif_label = QLabel("Notifications:\n- Exam on 15-Oct\n- Holiday on 20-Oct")
        notif_layout.addWidget(notif_label)
        notif_tab.setLayout(notif_layout)
        tabs.addTab(notif_tab, "Notifications")

    def send_message(self, text=None):
        query = text or self.input_field.text().strip()
        if not query:
            return
        self.chat_display.append(f"You: {query}")
        response = get_gemini_response(query)
        self.chat_display.append(f"Bot: {response}")
        self.input_field.clear()
        self.chat_display.verticalScrollBar().setValue(
            self.chat_display.verticalScrollBar().maximum()
        )

    def listen_voice(self):
        self.chat_display.append("🎤 Listening... Speak now (pause for 2–3 sec to send).")
        self.voice_thread = VoiceThread()
        self.voice_thread.recognized.connect(self.handle_voice_result)
        self.voice_thread.start()

    def handle_voice_result(self, text):
        if text.startswith(("⌛", "❌", "⚠️")):
            self.chat_display.append(text)
        else:
            self.send_message(text)

# === Run App ===
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = UniversityApp()
    win.show()
    sys.exit(app.exec_())
