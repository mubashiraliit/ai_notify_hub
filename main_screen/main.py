# main.py
import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QShortcut, QGraphicsDropShadowEffect, \
    QGraphicsBlurEffect
from PyQt5.QtGui import QFontDatabase, QFont, QKeySequence, QColor
from PyQt5.QtCore import QFile, QTextStream, Qt, QPoint, QRect

from ui import ui_MainWindow

# Importing chatbot
try:
    from Chatbot_project.chatbot_app import UniversityApp

    CHATBOT_IMPORTED = True
except ImportError as e:
    print(f"Chatbot import error: {e}")
    CHATBOT_IMPORTED = False

# file path set
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QSS_FILE = os.path.join(BASE_DIR, "styles.qss")
FONT_DIR = os.path.join(BASE_DIR, "assets", "fonts")
USER_FONT_DIR = r"E:\main_screen\assets\fonts"
USER_QSS_FILE = r"E:\main_screen\styles.qss"


# End file paths


# Fonts loading functions
def load_fonts(font_dir, fallback_dir):
    db = QFontDatabase()
    actual_font_dir = font_dir
    if not os.path.exists(actual_font_dir):
        if os.path.exists(fallback_dir):
            actual_font_dir = fallback_dir
        else:
            print(f"Font directory not found: {font_dir} OR {fallback_dir}")
            return

    count = 0
    loaded_families = set()
    for filename in os.listdir(actual_font_dir):
        if filename.lower().endswith(('.ttf', '.otf')):
            font_path = os.path.join(actual_font_dir, filename)
            font_id = db.addApplicationFont(font_path)
            if font_id != -1:
                count += 1
                families = db.applicationFontFamilies(font_id)
                if families:
                    loaded_families.add(families[0])
            else:
                print(f"Failed to load font file: {filename}")

    print(f"Attempted to load {count} font files from {actual_font_dir}.")
    if loaded_families:
        print(f"Successfully registered font families: {', '.join(loaded_families)}")


# End Font Loading


# Helper Function for Shadows
def apply_shadow(widget, blur=30, x_offset=0, y_offset=5, color_alpha=50):
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(blur)
    shadow.setXOffset(x_offset)
    shadow.setYOffset(y_offset)
    shadow.setColor(QColor(0, 0, 0, color_alpha))  # light black shadow
    widget.setGraphicsEffect(shadow)


# End Helper Function


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Smart Notice Board 2.0")
        self.showMaximized()

        # Chatbot Window Setup
        self.chatbot_window = None  # wont use non resources
        self.chatbot_geometry = None

        # Blur Effect Setup
        self.blur_effect = QGraphicsBlurEffect()
        self.blur_effect.setBlurRadius(5)  # adjust the blur values
        self.blur_effect.setEnabled(False)  # disable while starting
        self.ui.centralwidget.setGraphicsEffect(self.blur_effect)  #applying for the effects
        # End Blur Setup

        # F3 Global Shortcut Setup
        self.f3_shortcut = QShortcut(QKeySequence(Qt.Key_Left), self)  # Left Arrow
        self.f3_shortcut.setContext(Qt.ApplicationShortcut)
        self.f3_shortcut.activated.connect(self.toggle_chatbot)
        # End F3 Setup

    def toggle_chatbot(self):
        """Chatbot will show/closes."""
        if not CHATBOT_IMPORTED:
            print("Chatbot module not loaded. Key disabled.")
            return

        # Logic Fix: Close vs Show
        if self.chatbot_window and self.chatbot_window.isVisible():
            print("Closing chatbot...")
            self.blur_effect.setEnabled(False)  # Blur effect removing
            self.chatbot_window.close()
            self.chatbot_window = None
            self.activateWindow()

        elif self.chatbot_window is None:
            print("Starting chatbot...")
            self.blur_effect.setEnabled(True)  # adding blur effect

            self.chatbot_window = UniversityApp()

            self.chatbot_window.setWindowFlags(
                Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint
            )
            apply_shadow(self.chatbot_window)  # applying shadows

            # POSITION & HEIGHT FIX
            try:
                ai_card = self.ui.ai_card
                card_global_pos = ai_card.mapToGlobal(QPoint(0, 0))
                card_width = ai_card.size().width()

                footer = self.ui.footer
                footer_global_pos = footer.mapToGlobal(QPoint(0, 0))

                card_height = footer_global_pos.y() - card_global_pos.y()
                card_height = card_height - 10  # 10px padding from footer

                if card_global_pos.x() < 50 or card_height < 100:
                    raise Exception("Calculated position/height invalid, using fallback.")

                self.chatbot_geometry = QRect(card_global_pos.x(), card_global_pos.y(), card_width, card_height)
                print(f"Chatbot geometry calculated: {self.chatbot_geometry}")

            except Exception as e:
                print(f"Error calculating AI card geometry: {e}. Using fallback.")
                screen_geo = QApplication.desktop().availableGeometry(self)
                default_width = 380
                default_height = 500
                default_x = screen_geo.width() - default_width - 20
                default_y = screen_geo.height() - default_height - 20
                self.chatbot_geometry = QRect(default_x, default_y, default_width, default_height)

            self.chatbot_window.setGeometry(self.chatbot_geometry)
            self.chatbot_window.setFixedSize(self.chatbot_geometry.size())
            self.chatbot_window.show()
            self.chatbot_window.activateWindow()
            self.chatbot_window.setFocus()

    # Chatbot window close then the main screen is closed
    def closeEvent(self, event):
        if self.chatbot_window:
            self.chatbot_window.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 1. Fonts load
    load_fonts(FONT_DIR, USER_FONT_DIR)

    # 2. Stylesheet applying
    actual_qss_file = QSS_FILE
    if not os.path.exists(actual_qss_file):
        if os.path.exists(USER_QSS_FILE):
            actual_qss_file = USER_QSS_FILE
        else:
            print(f"Stylesheet not found: {QSS_FILE} OR {USER_QSS_FILE}")
            actual_qss_file = None

    if actual_qss_file:
        qss_file = QFile(actual_qss_file)
        if qss_file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(qss_file)
            stylesheet = stream.readAll()
            app.setStyleSheet(stylesheet)
            qss_file.close()
            print(f"Applied stylesheet from: {actual_qss_file}")
        else:
            print(f"Could not open stylesheet: {actual_qss_file}")

    # 3. Creating windows
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())