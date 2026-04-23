import sys
import os
import asyncio
import threading
import pygame
import speech_recognition as sr
from langdetect import detect
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel, QHBoxLayout,
    QScrollArea, QFrame
)
from PyQt5.QtCore import QThread, pyqtSignal, QObject, pyqtSlot, QMetaObject, Q_ARG, Qt, QSize, QTimer
from PyQt5.QtGui import QTextCursor, QFont, QMovie

import google.generativeai as genai
import edge_tts
from deep_translator import GoogleTranslator

#Constants and Setup


# API_KEY
API_KEY = "YOUR GEN AI API KEY"

try:
    genai.configure(api_key=API_KEY)
except Exception as e:
    print(f"Failed to configure Gemini: {e}")

#PATH FIX
CHATBOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(CHATBOT_DIR, "university_data.txt")
TTS_OUTPUT_FILE = os.path.join(CHATBOT_DIR, "voice_output.mp3")


def get_asset_path(asset_name: str) -> str | None:
    """Chatbot_project/assets/ folder se asset dhoondhega."""
    relative_path = os.path.join(CHATBOT_DIR, "assets", asset_name)
    if os.path.exists(relative_path):
        return relative_path
    else:
        print(f"Asset not found: {asset_name}")
        return None

#End Path Fix

#Load University Data
def load_data(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return "Error: university_data.txt not found."


UNIVERSITY_DATA = load_data(DATA_FILE)

# Background Worker Threads (Optimized)


class LanguageProcessor(QObject):
    finished = pyqtSignal(str)

    @pyqtSlot(str)
    def process(self, text):
        try:
            if any('\u0600' <= c <= '\u06FF' for c in text): self.finished.emit(text); return
            lang = detect(text)
            if lang == "en": self.finished.emit(text); return
            translated = GoogleTranslator(source='auto', target='ur').translate(text)
            self.finished.emit(translated or text)
        except Exception as e:
            print(f"Language handling error: {e}");
            self.finished.emit(text)


class GeminiWorker(QObject):
    response_ready = pyqtSignal(str);
    error = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent);
        self.model = None

    @pyqtSlot(str)
    def get_response(self, user_query):
        if self.model is None:
            try:
                self.model = genai.GenerativeModel("gemini-2.5-flash-lite")
            except Exception as e:
                self.error.emit(f"Failed to init Gemini: {e}"); return
# You can edit your system prompt as your use.
        system_prompt = f"""
    You are a helpful university assistant for GCUH (Government College University Hyderabad).
    Respond only to university-related queries.
    # If the user’s query is in English, respond in English.  
    # If the query is in Roman Urdu or native Urdu, respond in Urdu.
    If the user’s message is written in English, respond only in English.
    If the user’s message is written in Roman Urdu or Urdu, respond only in native Urdu script, just like normal Urdu writing — not in Roman Urdu.
    
    When replying in Urdu, write naturally as a native Urdu speaker (e.g.,
    User: "sir salman kiya parhata hai?"
    Response: "سر سلمان کیا پڑھاتے ہیں؟").
    
    Always treat the user’s message as a question or statement to be answered, not to be repeated.
    This rule is strict — never mix languages in a single response.
    
    Data: {UNIVERSITY_DATA}
    Response rules:
    1. If the query is NOT related to the university, reply: "Sorry, your query isn’t related to the university."
    2. If the query is related to the university but NOT related to the Computer Science department, reply: "Your query isn’t related to the Computer Science department."
    3. If the query is related to the university and CS department but the data is not available, reply: "Sorry, we don’t have this data right now. We’ll look into it and update it soon."
    4. If the query is related and data is available, respond helpfully using the given data.
    Always stay polite, clear, and concise.
    """
        try:
            full_prompt = f"{system_prompt}\nUser: {user_query}"
            response = self.model.generate_content(full_prompt)
            self.response_ready.emit(response.text if response.text else "No response.")
        except Exception as e:
            self.error.emit(f"Error communicating with Gemini: {str(e)}")


class VoiceInputThread(QThread):
    recognized = pyqtSignal(str);
    listening = pyqtSignal(str)

    def run(self):
        recognizer = sr.Recognizer();
        recognizer.energy_threshold = 150
        recognizer.dynamic_energy_threshold = True;
        recognizer.pause_threshold = 1.2
        with sr.Microphone() as source:
            try:
                self.listening.emit("🎙 Listening... please speak clearly.")
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)
                self.listening.emit("⌛ Processing voice...")
                text_en, text_ur = "", ""
                try:
                    text_en = recognizer.recognize_google(audio, language="en-US")
                except sr.UnknownValueError:
                    pass
                try:
                    text_ur = recognizer.recognize_google(audio, language="ur-PK")
                except sr.UnknownValueError:
                    pass
                final_query = text_ur if len(text_ur) > len(text_en) else text_en
                final_query = final_query.strip()
                if not final_query:
                    self.recognized.emit("❌ Could not understand your voice.")
                else:
                    self.recognized.emit(final_query)
            except sr.WaitTimeoutError:
                self.recognized.emit("⌛ Listening timed out.")
            except Exception as e:
                self.recognized.emit(f"⚠️ Error: {str(e)}")


class TtsThread(QThread):
    finished = pyqtSignal();
    error = pyqtSignal(str)

    def __init__(self, text_to_speak, parent=None):
        super().__init__(parent);
        self.text_to_speak = text_to_speak

    def run(self):
        try:
            asyncio.run(self.generate_and_play()); self.finished.emit()
        except Exception as e:
            self.error.emit(f"TTS Error: {e}")

    async def generate_and_play(self):
        lang = "urdu" if any('\u0600' <= c <= '\u06FF' for c in self.text_to_speak) else "english"
        voice = "ur-PK-AsadNeural" if lang == "urdu" else "en-US-JennyNeural"
        communicate = edge_tts.Communicate(self.text_to_speak, voice)
        await communicate.save(TTS_OUTPUT_FILE)
        self.play_audio_sync()

    def play_audio_sync(self):
        try:
            pygame.mixer.init();
            pygame.mixer.music.load(TTS_OUTPUT_FILE)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy(): pygame.time.Clock().tick(10)
        except Exception as e:
            print(f"Audio playback error: {e}")
        finally:
            pygame.mixer.quit()
            if os.path.exists(TTS_OUTPUT_FILE):
                try:
                    os.remove(TTS_OUTPUT_FILE)
                except PermissionError:
                    pass

# PyQt App (UI Redesigned)


class UniversityApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("University Chatbot")

        # BORDER RADIUS FIX
        # Transparenting windows
        self.setAttribute(Qt.WA_TranslucentBackground)
        # END BORDER RADIUS FIX

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_widget.setObjectName("mainWidget")

        # New chat Ui
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)  # ✅ Spacing kam ki

        # 1. Chat History (Scroll Area)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("scrollArea")
        self.scroll_area.setFrameShape(QFrame.NoFrame)

        scroll_content_widget = QWidget()
        scroll_content_widget.setObjectName("scrollContent")
        self.chat_history_layout = QVBoxLayout(scroll_content_widget)
        self.chat_history_layout.setAlignment(Qt.AlignTop)
        self.chat_history_layout.setSpacing(8)  # ✅ Spacing kam ki

        self.scroll_area.setWidget(scroll_content_widget)
        layout.addWidget(self.scroll_area, 1)  # 1 = Stretch

        # 2. Listening GIF
        self.listening_gif_label = QLabel()
        self.listening_gif_label.setAlignment(Qt.AlignCenter)
        gif_path = get_asset_path("listening.gif")
        if gif_path:
            self.listening_movie = QMovie(gif_path)
            self.listening_movie.setScaledSize(QSize(120, 120))  # ✅ GIF chota
            self.listening_gif_label.setMovie(self.listening_movie)
            self.listening_movie.start()
        else:
            self.listening_gif_label.setText("... (GIF not found) ...")

        self.listening_gif_label.setFixedHeight(85)  # ✅ Height kam ki
        layout.addWidget(self.listening_gif_label, 0)  # 0 = No stretch

        # 3. Listening Text
        self.listening_text_label = QLabel("Press '0' to Speak")
        self.listening_text_label.setAlignment(Qt.AlignCenter)
        self.listening_text_label.setObjectName("listeningText")
        self.listening_text_label.setFixedHeight(20)  # ✅ Height kam ki
        layout.addWidget(self.listening_text_label, 0)  # 0 = No stretch

        self.show_listening_ui(False)

        self.apply_stylesheet()

        #Setup Background Threads
        self.setup_threads()
        self.tts_thread = None
        self.voice_thread = None
        self.is_listening = False

        #UI Helpers (New functions)

    def show_listening_ui(self, is_listening):
        """Chat history ya listening GIF ko show/hide karega."""
        if is_listening:
            self.scroll_area.hide()
            self.listening_gif_label.show()
            self.listening_text_label.show()
            self.listening_text_label.setText("🎙 Listening...")
        else:
            self.scroll_area.show()
            self.listening_gif_label.hide()
            self.listening_text_label.show()
            self.listening_text_label.setText("Press '0' to Speak")

    def add_message(self, text, user_type):
        """will add new message on chat history."""

        title = "User" if user_type == "User" else "Uni Assistant"

        title_label = QLabel(f"{title}:")
        if user_type == "User":
            title_label.setObjectName("chatTitleUser")
        else:
            title_label.setObjectName("chatTitleAssistant")

        message_frame = QFrame()
        frame_layout = QVBoxLayout(message_frame)
        frame_layout.setContentsMargins(8, 8, 8, 8)

        if user_type == "User":
            message_frame.setObjectName("chatFrameUser")
        else:
            message_frame.setObjectName("chatFrameAssistant")

        message_label = QLabel(text)
        message_label.setObjectName("chatMessageLabel")
        message_label.setWordWrap(True)
        frame_layout.addWidget(message_label)

        self.chat_history_layout.addWidget(title_label)
        self.chat_history_layout.addWidget(message_frame)

        self.scroll_to_bottom()

    def replace_last_message(self, new_text, user_type):
        """"replacing the thinking message to new"""
        try:
            last_title_label = self.chat_history_layout.itemAt(self.chat_history_layout.count() - 2).widget()
            last_title_label.setText("Uni Assistant:")
            last_title_label.setObjectName("chatTitleAssistant")

            last_frame = self.chat_history_layout.itemAt(self.chat_history_layout.count() - 1).widget()
            message_label = last_frame.findChild(QLabel)
            message_label.setText(new_text)

            if user_type == "bot_error":
                last_frame.setObjectName("chatFrameError")
            else:
                last_frame.setObjectName("chatFrameAssistant")

            last_frame.setStyleSheet(self.styleSheet())
            last_title_label.setStyleSheet(self.styleSheet())
        except Exception as e:
            print(f"Error replacing message: {e}")
            self.add_message(new_text, user_type)

        self.scroll_to_bottom()

    def scroll_to_bottom(self):
        """Auto-scrolls to the latest message."""
        QTimer.singleShot(100, lambda: self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()))

    # Threading & Logic (Updated)

    def setup_threads(self):
        self.lang_thread = QThread();
        self.lang_processor = LanguageProcessor()
        self.lang_processor.moveToThread(self.lang_thread)
        self.lang_processor.finished.connect(self.start_gemini_processing)
        self.lang_thread.start()

        self.gemini_thread = QThread();
        self.gemini_worker = GeminiWorker()
        self.gemini_worker.moveToThread(self.gemini_thread)
        self.gemini_worker.response_ready.connect(self.handle_gemini_response)
        self.gemini_worker.error.connect(self.handle_processing_error)
        self.gemini_thread.start()

    @pyqtSlot(str)
    def start_gemini_processing(self, processed_query):
        self.add_message("⌛ Thinking...", "Uni Assistant")
        QMetaObject.invokeMethod(self.gemini_worker, "get_response", Qt.QueuedConnection, Q_ARG(str, processed_query))

    @pyqtSlot(str)
    def handle_gemini_response(self, response):
        self.replace_last_message(response, "bot")
        self.start_tts(response)

    @pyqtSlot(str)
    def handle_processing_error(self, error_message):
        self.replace_last_message(error_message, "bot_error")
        self.show_listening_ui(False)
        self.is_listening = False

    def start_tts(self, text):
        if self.tts_thread and self.tts_thread.isRunning():
            self.tts_thread.terminate()
        self.tts_thread = TtsThread(text_to_speak=text, parent=self)
        self.tts_thread.error.connect(lambda e: print(e))
        self.tts_thread.finished.connect(lambda: self.show_listening_ui(False))
        self.tts_thread.start()

    @pyqtSlot()
    def start_voice_recognition(self):
        if self.is_listening:
            return

        self.is_listening = True
        self.show_listening_ui(True)

        self.voice_thread = VoiceInputThread(self)
        self.voice_thread.listening.connect(lambda msg: self.listening_text_label.setText(msg))
        self.voice_thread.recognized.connect(self.handle_voice_result)
        self.voice_thread.finished.connect(self.on_voice_finished)
        self.voice_thread.start()

    @pyqtSlot(str)
    def handle_voice_result(self, result):
        self.is_listening = False
        self.show_listening_ui(False)

        if result.startswith(("❌", "⚠️", "⌛")):
            self.add_message(result, "Uni Assistant")
        else:
            self.add_message(result, "User")
            QMetaObject.invokeMethod(self.lang_processor, "process", Qt.QueuedConnection, Q_ARG(str, result))

    @pyqtSlot()
    def on_voice_finished(self):
        self.is_listening = False
        self.show_listening_ui(False)

    def keyPressEvent(self, event):
        """when the chatbot window active then detect the press key."""
        if event.key() == Qt.Key_0:  # Agar '0' key dabi
            print(" '0' key pressed, starting voice recognition...")
            self.start_voice_recognition()
        else:
            super().keyPressEvent(event)

    def closeEvent(self, event):
        """clening the threads when windows is closed."""
        print("Chatbot closeEvent called. Cleaning up threads...")
        self.lang_thread.quit();
        self.lang_thread.wait()
        self.gemini_thread.quit();
        self.gemini_thread.wait()

        if self.tts_thread and self.tts_thread.isRunning():
            print("Terminating TTS thread...")
            self.tts_thread.terminate();
            self.tts_thread.wait()

        if self.voice_thread and self.voice_thread.isRunning():
            print("Terminating active voice thread...")
            self.voice_thread.terminate();
            self.voice_thread.wait()

        event.accept()

    def apply_stylesheet(self):
        """for new ui stylesheet."""
        self.setStyleSheet("""
            #mainWidget {
                background-color: #f8f8f8; 
                font-family: "Poppins", sans-serif;
                border: 3px solid #7b1515;
                border-radius: 10px; /* ✅ Aapka border radius */
            }
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            #scrollContent {
                background-color: transparent;
            }

            /* --- Titles --- */
            QLabel#chatTitleUser, QLabel#chatTitleAssistant {
                font-family: "Poppins";
                font-weight: 600; 
                font-size: 9pt; /* ✅ Chota kiya */
                color: #333;
                margin-left: 5px;
                margin-bottom: 1px; 
            }

            /* --- Message Boxes (Frames) --- */
            QFrame#chatFrameUser {
                background-color: #7b1515; /* Maroon */
                border-radius: 8px; 
            }
            QFrame#chatFrameAssistant {
                background-color: #AF8F6D; /* Brown/Orange */
                border-radius: 8px;
            }
            QFrame#chatFrameError {
                background-color: #FFEBEE; /* Light Red */
                border: 1px solid #B71C1C;
                border-radius: 8px;
            }

            /* --- Message Text (Labels) --- */
            QFrame#chatFrameUser QLabel, QFrame#chatFrameAssistant QLabel {
                color: white;
                font-size: 8pt; /* ✅ Chota kiya */
                font-family: "Poppins";
            }
            QFrame#chatFrameError QLabel {
                color: #B71C1C; /* Dark Red */
                font-size: 8pt; /* ✅ Chota kiya */
                font-family: "Poppins";
            }

            /* --- Listening UI --- */
            QLabel#listeningText {
                font-family: "Poppins";
                font-weight: bold;
                font-size: 10pt; /* ✅ Chota kiya */
                color: #555;
            }
        """)
# Run Application for testing

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UniversityApp()
    window.show()
    sys.exit(app.exec_())