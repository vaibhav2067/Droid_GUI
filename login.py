# patient_login.py

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton,
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit
)
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt, QEvent

from virtual_keyboard import VirtualKeyboard  # 🧩 Importing Virtual Keyboard

# ===== BACKGROUND WIDGET =====
class BackgroundWidget(QWidget):
    def __init__(self, background_path):
        super().__init__()
        self.background_pixmap = QPixmap(background_path)

    def paintEvent(self, event):
        painter = QPainter(self)
        scaled_pixmap = self.background_pixmap.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        painter.drawPixmap(self.rect(), scaled_pixmap)

# ===== MAIN WINDOW =====
class FullscreenWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.showFullScreen()

        self.background_widget = BackgroundWidget("coolbackgrounds-topography-micron.jpg")
        self.setCentralWidget(self.background_widget)

        main_layout = QVBoxLayout()
        self.background_widget.setLayout(main_layout)

        # Top Bar
        top_bar = QHBoxLayout()
        logo_label = QLabel()
        pixmap = QPixmap("icons/LOGO_edited_edited.png")
        logo_label.setPixmap(pixmap)
        logo_label.setFixedSize(160, 80)
        logo_label.setScaledContents(True)
        logo_label.setStyleSheet("background: transparent;")
        top_bar.addWidget(logo_label)
        top_bar.addStretch()
        support_button = QPushButton("Support")
        support_button.setFixedSize(100, 40)
        top_bar.addWidget(support_button)

        # Login Layout
        login_layout = QVBoxLayout()
        login_layout.setSpacing(10)
        login_layout.setAlignment(Qt.AlignCenter)

        username_label = QLabel("Username:")
        username_label.setStyleSheet("color: white; font-size: 18px;")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setFixedWidth(300)
        self.username_input.setStyleSheet("""
            padding: 10px;
            font-size: 18px;
            background-color: rgba(255, 255, 255, 0);
            color: white;
            border: none;
            border-bottom: 2px solid white;
        """)

        password_label = QLabel("Password:")
        password_label.setStyleSheet("color: white; font-size: 18px;")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedWidth(300)
        self.password_input.setStyleSheet("""
            padding: 10px;
            font-size: 18px;
            background-color: rgba(255, 255, 255, 0);
            color: white;
            border: none;
            border-bottom: 2px solid white;
        """)

        login_button = QPushButton("Login")
        login_button.setFixedWidth(150)
        login_button.setFixedHeight(40)

        login_layout.addWidget(username_label)
        login_layout.addWidget(self.username_input)
        login_layout.addWidget(password_label)
        login_layout.addWidget(self.password_input)
        login_layout.addWidget(login_button, alignment=Qt.AlignCenter)

        # Bottom Bar
        bottom_bar = QHBoxLayout()
        power_button = QPushButton("Power Off")
        power_button.setFixedSize(120, 40)
        bottom_bar.addWidget(power_button)
        bottom_bar.addStretch()

        # Virtual Keyboard
        self.keyboard = VirtualKeyboard()
        self.keyboard.hide()

        main_layout.addLayout(top_bar)
        main_layout.addLayout(login_layout, stretch=1)
        main_layout.addWidget(self.keyboard)
        main_layout.addLayout(bottom_bar)

        self.username_input.installEventFilter(self)
        self.password_input.installEventFilter(self)

    def eventFilter(self, source, event):
        if event.type() == QEvent.FocusIn and isinstance(source, QLineEdit):
            self.keyboard.input_target = source
            self.keyboard.show()
        return super().eventFilter(source, event)

# ===== MAIN EXECUTION =====
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FullscreenWindow()
    window.show()
    sys.exit(app.exec_())
