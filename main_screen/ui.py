import os
import json
from PyQt5.QtWidgets import (
    QWidget, QMainWindow, QLabel, QPushButton, QFrame,
    QVBoxLayout, QHBoxLayout, QGridLayout, QSizePolicy,
    QGraphicsDropShadowEffect
)
from PyQt5.QtCore import (
    Qt, QSize, QTimer, QUrl, QObject,
    pyqtSlot
)
from PyQt5.QtGui import QFont, QColor, QPixmap, QIcon, QImage
from PyQt5.QtNetwork import (
    QNetworkAccessManager,
    QNetworkRequest,
    QNetworkReply
)

#  Helper Functions (Shadow, Heading, Icon Path)

def apply_shadow(widget, blur=25, x_offset=0, y_offset=2, color_alpha=40):
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(blur)
    shadow.setXOffset(x_offset)
    shadow.setYOffset(y_offset)
    shadow.setColor(QColor(0, 0, 0, color_alpha))
    widget.setGraphicsEffect(shadow)

def create_underlined_heading(text: str) -> QWidget:
    container = QWidget()
    layout = QVBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 2)
    layout.setSpacing(0)
    label = QLabel(text)
    label.setObjectName("heading_text_label")
    label.setFont(QFont("Poppins", 20, QFont.Bold))
    underline = QFrame()
    underline.setObjectName("heading_underline_frame")
    underline.setFixedHeight(4)
    underline.setFixedWidth(80)
    layout.addWidget(label)
    layout.addWidget(underline)
    container.setFixedHeight(48)
    return container

def get_icon_path(icon_name: str) -> str | None:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    relative_path = os.path.join("images", icon_name)
    fallback_path = os.path.join(r"E:\main_screen", "images", icon_name)
    if os.path.exists(relative_path):
        return relative_path
    elif os.path.exists(fallback_path):
        return fallback_path
    else:
        print(f"Icon/Image not found: {icon_name}")
        return None

#MAIN UI CLASS (UPDATED)

class Ui2_MainWindow(QObject): 

    API_BASE_URL = "http://localhost:5000"

    def setupUi(self, MainWindow: QMainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1366, 768)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        self.root_layout = QVBoxLayout(self.centralwidget)
        self.root_layout.setContentsMargins(10, 10, 10, 10)
        self.root_layout.setSpacing(10)

        main_grid = QHBoxLayout()
        main_grid.setSpacing(10)

        # LEFT COLUMN
        left_col = QVBoxLayout()
        left_col.setSpacing(20)

        # Logo + University name (Same as before)
        logo_frame = QFrame()
        logo_frame.setObjectName("card")
        apply_shadow(logo_frame)
        logo_layout = QVBoxLayout(logo_frame)
        logo_layout.setAlignment(Qt.AlignCenter)
        self.logo_label = QLabel()
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.logo_label.setFixedSize(130, 130)
        self.logo_label.setObjectName("logo_label")
        self.logo_label.setScaledContents(True)
        logo_path = get_icon_path("gclogo.png")
        if logo_path:
            self.logo_label.setPixmap(QPixmap(logo_path))
        else:
            self.logo_label.setText("LOGO\n(Not Found)")
            self.logo_label.setFont(QFont("Poppins", 10))
        self.univ_label = QLabel("GC UNIVERSITY HYDERABAD")
        self.univ_label.setObjectName("univ_label")
        self.univ_label.setAlignment(Qt.AlignCenter)
        self.univ_label.setFont(QFont("Poppins", 15, QFont.Bold))
        logo_layout.addStretch(1)
        logo_layout.addWidget(self.logo_label, 0, Qt.AlignCenter)
        logo_layout.addWidget(self.univ_label, 0, Qt.AlignCenter)
        logo_layout.addStretch(1)
        left_col.addWidget(logo_frame) # Logo form not centering

        #Academic Notices
        self.notice_title_button = QPushButton(" ACADEMIC NOTICES")
        self.notice_title_button.setObjectName("notice_title_button")
        self.notice_title_button.setFont(QFont("Poppins", 13, QFont.Bold))
        self.notice_title_button.setFixedHeight(45)
        icon1_path = get_icon_path("icon1.png")
        if icon1_path:
            self.notice_title_button.setIcon(QIcon(icon1_path))
            self.notice_title_button.setIconSize(QSize(24, 24))
        left_col.addWidget(self.notice_title_button)

        # Create empty labels for notices (2 slots)
        self.notice_labels = [] 
        for i in range(2):
            frame = QFrame()
            frame.setObjectName("notice_card")
            apply_shadow(frame)
            frame.setFixedSize(190, 290) # Size fixed
            inner_layout = QVBoxLayout(frame)
            inner_layout.setContentsMargins(5, 5, 5, 5)
            
            img_label = QLabel("Loading...")
            img_label.setAlignment(Qt.AlignCenter)
            img_label.setScaledContents(True)
            img_label.setFont(QFont("Poppins", 11, QFont.Bold))
            img_label.setStyleSheet("background-color: #f8f8f8; color: #999; border: 1px dashed #ccc;")

            inner_layout.addWidget(img_label)
            self.notice_labels.append(img_label)

            left_col.addWidget(frame, 0, Qt.AlignCenter)

        main_grid.addLayout(left_col, 3)

        #CENTER COLUMN
        center_col = QVBoxLayout()
        center_col.setSpacing(8)

        # Daily Quote
        quote_card = QFrame()
        quote_card.setObjectName("card")
        apply_shadow(quote_card)
        qlayout = QVBoxLayout(quote_card)
        qlayout.setContentsMargins(12, 10, 12, 10)
        self.quote_title = create_underlined_heading("DAILY QUOTE")
        self.quote_text = QLabel("Loading Daily Quote...")
        self.quote_text.setObjectName("quote_text")
        self.quote_text.setWordWrap(True)
        self.quote_text.setFont(QFont("Poppins", 14, QFont.StyleItalic))
        qlayout.addWidget(self.quote_title)
        qlayout.addWidget(self.quote_text)
        quote_card.setMinimumHeight(100)
        center_col.addWidget(quote_card, 0)

        # Important Alerts
        alerts_card = QFrame()
        alerts_card.setObjectName("alerts_card")
        apply_shadow(alerts_card)
        alayout = QVBoxLayout(alerts_card)
        alayout.setContentsMargins(12, 10, 12, 10)
        self.alerts_title = create_underlined_heading("IMPORTANT ALERTS")
        self.alerts_text = QLabel("Loading alerts...")
        self.alerts_text.setObjectName("maroon_body_text")
        self.alerts_text.setWordWrap(True)
        self.alerts_text.setFont(QFont("Poppins", 11))
        alayout.addWidget(self.alerts_title)
        alayout.addWidget(self.alerts_text)
        alerts_card.setMinimumHeight(120)
        center_col.addWidget(alerts_card, 0)

        # Department Timetables
        dept_card = QFrame()
        dept_card.setObjectName("card")
        apply_shadow(dept_card)
        dlayout = QVBoxLayout(dept_card)
        dlayout.setSpacing(4)
        dlayout.setContentsMargins(8, 5, 8, 8)
        self.dept_title = create_underlined_heading("DEPARTMENT TIMETABLES")
        dlayout.addWidget(self.dept_title)
        
        self.timetable_labels = [] 
        grid = QGridLayout()
        grid.setSpacing(15)

        for i in range(4):
            box = QFrame()
            box.setObjectName("timetable_card")
            apply_shadow(box)
            box.setFixedSize(350, 240)
            inner_layout = QVBoxLayout(box)
            inner_layout.setContentsMargins(5, 5, 5, 5)
            img_label = QLabel()
            img_label.setAlignment(Qt.AlignCenter)
            img_label.setScaledContents(True)
            img_label.setStyleSheet("background-color: #c4c4c4; border-radius: 10px;")
            img_label.setFixedSize(335, 220)
            inner_layout.addWidget(img_label)
            self.timetable_labels.append(img_label)
            grid.addWidget(box, i // 2, i % 2)

        dlayout.addLayout(grid)
        center_col.addWidget(dept_card, 1)
        main_grid.addLayout(center_col, 12)

        # RIGHT COLUMN
        right_col = QVBoxLayout()
        right_col.setSpacing(10)
        right_col.setAlignment(Qt.AlignTop)

        # Exam Updates
        exam_card = QFrame()
        exam_card.setObjectName("card")
        apply_shadow(exam_card)
        exam_layout = QVBoxLayout(exam_card)
        exam_layout.setContentsMargins(10, 6, 10, 6)
        self.exam_title = create_underlined_heading("EXAM UPDATES")
        self.exam_text = QLabel("Loading...")
        self.exam_text.setObjectName("maroon_body_text")
        self.exam_text.setWordWrap(True)
        self.exam_text.setFont(QFont("Poppins", 5))
        self.exam_text.setStyleSheet("color: #800000;font-size: 19px;")
      
        exam_layout.addWidget(self.exam_title)
        exam_layout.addWidget(self.exam_text)
        exam_card.setMinimumHeight(100)
        right_col.addWidget(exam_card, 0)

        # Student Achievements
        ach_card = QFrame()
        ach_card.setObjectName("card")
        apply_shadow(ach_card)
        self.ach_layout = QVBoxLayout(ach_card)
        self.ach_layout.setContentsMargins(12, 8, 12, 8)
        self.ach_layout.setSpacing(6)

        self.ach_title = create_underlined_heading("STUDENTS ACHIEVEMENTS")
        self.ach_layout.addWidget(self.ach_title)
        self.ach_labels = []

        self.ach_layout.addStretch()
        right_col.addWidget(ach_card, 1)


        #AI Assistant
        self.ai_card = QFrame()
        self.ai_card.setObjectName("card")
        apply_shadow(self.ai_card)
        ai_layout = QVBoxLayout(self.ai_card)
        ai_layout.setContentsMargins(12, 8, 12, 8)
        ai_layout.setSpacing(10)
        self.ai_title = create_underlined_heading("AI ASSISTANT")
        self.ai_desc = QLabel(
            "This AI-based University Assistant is built to provide accurate answers "
            "within a given academic context. It helps display relevant information and "
            "respond to student queries. Users can interact with the system for academic,"
            " timetable, and notice board-related questions. Simply press the button below "
            "to start speaking."
        )
        self.ai_desc.setObjectName("normal_text")
        self.ai_desc.setWordWrap(True)
        self.ai_desc.setStyleSheet("QLabel { font-family: 'Poppins'; font-size: 17px; color: #222; line-height: 1.2em; }")
        self.ai_button = QPushButton("PRESS DOWN BUTTON TO SPEAK")
        self.ai_button.setObjectName("ai_button")
        self.ai_button.setFont(QFont("Poppins", 12, QFont.Bold))
        self.ai_button.setFixedHeight(45)
        icon2_path = get_icon_path("icon2.png")
        if icon2_path:
            self.ai_button.setIcon(QIcon(icon2_path))
            self.ai_button.setIconSize(QSize(28, 28))
        ai_layout.addWidget(self.ai_title)
        ai_layout.addWidget(self.ai_desc, 1)
        ai_layout.addWidget(self.ai_button, 0, Qt.AlignBottom)
        self.ai_card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        right_col.addWidget(self.ai_card, 1)

        main_grid.addLayout(right_col, 4)

        #  Footer
        self.footer = QLabel("GC University Hyderabad, Kali Mori Hyderabad Sindh, Pakistan - Phone: 022-2111856")
        self.footer.setObjectName("footer")
        self.footer.setAlignment(Qt.AlignCenter)
        self.footer.setFont(QFont("Poppins", 10))

        self.root_layout.addLayout(main_grid, 1)
        self.root_layout.addWidget(self.footer, 0, Qt.AlignBottom)
        
        
        # REAL-TIME UPDATE CODE

        self.current_data_cache = {
            "notices": [],
            "quote": "",
            "alert": "",
            "timetables": [],
            "exam_date": "",
            "achievements": []
        }
        self.network_manager = QNetworkAccessManager(MainWindow)
        self.data_update_timer = QTimer(MainWindow)
        self.data_update_timer.timeout.connect(self.fetch_all_data)
        self.data_update_timer.start(10000) # 10 seconds
        self.fetch_all_data()
        
    # END OF setupUi

    def fetch_all_data(self):
        """Timer will call the whole apis."""
        print("--- [Timer Triggered] Checking for all API data... ---")
        self.fetch_api_text(f"{self.API_BASE_URL}/api/quotes", self.on_quotes_ready)
        self.fetch_api_text(f"{self.API_BASE_URL}/api/alertnotices", self.on_alert_ready)
        self.fetch_api_text(f"{self.API_BASE_URL}/api/exam-dates", self.on_exam_ready)
        self.fetch_api_text(f"{self.API_BASE_URL}/api/achievements", self.on_achievements_ready)
        self.fetch_api_text(f"{self.API_BASE_URL}/api/notices", self.on_notices_ready)
        self.fetch_api_text(f"{self.API_BASE_URL}/api/timetable", self.on_timetables_ready)

    def fetch_api_text(self, url, callback_slot):
        """Helper function: Text/JSON data fetch."""
        try:
            reply = self.network_manager.get(QNetworkRequest(QUrl(url)))
            reply.finished.connect(lambda: callback_slot(reply))
        except Exception as e:
            print(f"API request failed to start for {url}: {e}")

    def fetch_image(self, url, label_widget: QLabel):
        try:
            reply = self.network_manager.get(QNetworkRequest(QUrl(url)))
            reply.finished.connect(lambda: self.on_image_ready(reply, label_widget))
        except Exception as e:
            print(f"Image request failed to start for {url}: {e}")

    # NEW "SLOT" FUNCTIONS (DATA MILNE PAR CHALTE HAIN)

    @pyqtSlot(QNetworkReply)
    def on_quotes_ready(self, reply: QNetworkReply):
        if reply.error() == QNetworkReply.NoError:
            try:
                data = json.loads(bytes(reply.readAll()).decode('utf-8'))
                new_quote = f'"{data["quotes"]}"'
                if new_quote != self.current_data_cache["quote"]:
                    print("✅ UPDATING: Daily Quote")
                    self.quote_text.setText(new_quote)
                    self.current_data_cache["quote"] = new_quote
            except Exception as e:
                print(f"Quote JSON parse error: {e}")
        reply.deleteLater()

    @pyqtSlot(QNetworkReply)
    def on_alert_ready(self, reply: QNetworkReply):
        if reply.error() == QNetworkReply.NoError:
            try:
                data = json.loads(bytes(reply.readAll()).decode('utf-8'))
                new_alert = "No current alerts."
                if isinstance(data, list) and len(data) > 0:
                    new_alert = data[0].get("text", new_alert)
                if new_alert != self.current_data_cache["alert"]:
                    print("✅ UPDATING: Alert Text")
                    self.alerts_text.setText(new_alert)
                    self.current_data_cache["alert"] = new_alert
            except Exception as e:
                print(f"Alert JSON parse error: {e}")
        reply.deleteLater()

    @pyqtSlot(QNetworkReply)
    def on_exam_ready(self, reply: QNetworkReply):
        if reply.error() == QNetworkReply.NoError:
            try:
                data = json.loads(bytes(reply.readAll()).decode('utf-8'))
                new_exam_text = "N/A"
                if isinstance(data, list) and len(data) > 0:
                    new_exam_text = data[0].get("date", new_exam_text)
                if new_exam_text != self.current_data_cache["exam_date"]:
                    print("✅ UPDATING: Exam Date")
                    self.exam_text.setText(new_exam_text.title())
                    self.current_data_cache["exam_date"] = new_exam_text
            except Exception as e:
                print(f"Exam JSON parse error: {e}")
        reply.deleteLater()

    @pyqtSlot(QNetworkReply)
    def on_achievements_ready(self, reply: QNetworkReply):
        if reply.error() == QNetworkReply.NoError:
            try:
                data = json.loads(bytes(reply.readAll()).decode('utf-8'))
                new_achievements = []
                if isinstance(data, list) and len(data) > 0:
                    new_achievements = [item["achievement"] for item in data if "achievement" in item]
                if new_achievements != self.current_data_cache["achievements"]:
                    print("✅ UPDATING: Achievements List")
                    for label in self.ach_labels:
                        label.deleteLater()
                    self.ach_labels.clear()
                    loading_lbl = self.ach_layout.findChild(QLabel, "achievement_loading_label")
                    if loading_lbl:
                        loading_lbl.deleteLater()
                    for text in new_achievements:
                        item_frame = QFrame()
                        item_frame.setObjectName("achievement_item_frame")
                        item_layout = QVBoxLayout(item_frame)
                        item_layout.setContentsMargins(8, 6, 8, 6)
                        lbl = QLabel(text.capitalize())
                        lbl.setWordWrap(True)
                        lbl.setFont(QFont("Poppins", 8))
                        item_layout.addWidget(lbl)
                        self.ach_layout.insertWidget(self.ach_layout.count() - 1, item_frame)
                        self.ach_labels.append(item_frame)
                    self.current_data_cache["achievements"] = new_achievements
            except Exception as e:
                print(f"Achievements JSON parse error: {e}")
        reply.deleteLater()

    @pyqtSlot(QNetworkReply)
    def on_notices_ready(self, reply: QNetworkReply):
        if reply.error() == QNetworkReply.NoError:
            try:
                data = json.loads(bytes(reply.readAll()).decode('utf-8'))
                new_notice_urls = []
                if isinstance(data, list):
                    for item in data:
                        img_rel_path = item.get("image", "").replace("\\", "/")
                        full_url = f"{self.API_BASE_URL}/{img_rel_path}"
                        new_notice_urls.append(full_url)
                if new_notice_urls != self.current_data_cache["notices"]:
                    print("✅ UPDATING: Notice Images")
                    self.current_data_cache["notices"] = new_notice_urls
                    for i, label in enumerate(self.notice_labels):
                        if i < len(new_notice_urls):
                            self.fetch_image(new_notice_urls[i], label)
                        else:
                            label.clear()
                            label.setText("")
                            label.setStyleSheet("background-color: #f8f8f8; color: #999; border: 1px dashed #ccc;")
            except Exception as e:
                print(f"Notices JSON parse error: {e}")
        reply.deleteLater()

    @pyqtSlot(QNetworkReply)
    def on_timetables_ready(self, reply: QNetworkReply):
        if reply.error() == QNetworkReply.NoError:
            try:
                data = json.loads(bytes(reply.readAll()).decode('utf-8'))
                new_tt_urls = []
                if isinstance(data, list):
                    for item in data:
                        img_rel_path = item.get("image", "").replace("\\", "/")
                        full_url = f"{self.API_BASE_URL}/{img_rel_path}"
                        new_tt_urls.append(full_url)
                if new_tt_urls != self.current_data_cache["timetables"]:
                    print("✅ UPDATING: Timetable Images")
                    self.current_data_cache["timetables"] = new_tt_urls
                    for i, label in enumerate(self.timetable_labels):
                        if i < len(new_tt_urls):
                            self.fetch_image(new_tt_urls[i], label)
                        else:
                            label.clear()
                            label.setStyleSheet("background-color: #c4c4c4; border-radius: 10px;")
                            label.setFixedSize(335, 220)
            except Exception as e:
                print(f"Timetables JSON parse error: {e}")
        reply.deleteLater()

    @pyqtSlot(QNetworkReply, QLabel)
    def on_image_ready(self, reply: QNetworkReply, label_widget: QLabel):
        if reply.error() == QNetworkReply.NoError:
            image_data = reply.readAll()
            image = QImage()
            if image.loadFromData(image_data):
                pixmap = QPixmap(image)
                label_widget.setPixmap(pixmap.scaled(
                    label_widget.size(), 
                    Qt.KeepAspectRatio, 
                    Qt.SmoothTransformation
                ))
                label_widget.setStyleSheet("")
            else:
                label_widget.setText("⚠️ Invalid Image")
                print("Downloaded data was not a valid image.")
        else:
            label_widget.setText("⚠️ Load Failed")
            print(f"Image download error: {reply.errorString()}")
        reply.deleteLater()

#for testing
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui2_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())