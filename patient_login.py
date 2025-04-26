import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton,
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QGridLayout, QSizePolicy
)
from PyQt5.QtGui import QPixmap, QPainter, QIcon
from PyQt5.QtCore import Qt, QEvent


# ===== VIRTUAL KEYBOARD CLASS =====
class VirtualKeyboard(QWidget):
    def __init__(self, input_target=None):
        super().__init__()
        self.input_target = input_target
        self.caps_lock = False
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        hbox = QHBoxLayout()  # Horizontal box to center the grid
        hbox.setAlignment(Qt.AlignCenter)

        self.grid = QGridLayout()
        hbox.addLayout(self.grid)  # Place grid in the center
        layout.addLayout(hbox)


        self.keys = [
            ['~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+'],
            ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'Backspace'],
            ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']'],
            ['Caps', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', '\'', 'Enter'],
            ['Done', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', '\\'],
            ['Space']
        ]

        icon_map = {
            'Backspace': QIcon("icons/camera_icon_white.png"),
            'Enter': QIcon("icons/camera_icon_white.png"),
            'Caps': QIcon("icons/camera_icon_white.png"),
            'Space': QIcon("icons/camera_icon_white.png"),
            'Done': QIcon("icons/camera_icon_white.png")
        }

        row = 0
        for key_row in self.keys:
            col = 0
            for key in key_row:
                button = QPushButton()
                button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

                if key in icon_map:
                    button.setIcon(icon_map[key])
                    button.setIconSize(button.sizeHint())
                else:
                    button.setText(key.upper() if len(key) == 1 else key)

                # Special styling for function keys
                if key in ['Backspace', 'Enter', 'Caps', 'Done', 'Space']:
                    button.setStyleSheet("""
                        QPushButton {
                            background-color: #34495e;
                            color: white;
                            border-radius: 10px;
                            font-size: 16px;
                            padding: 10px;
                            margin: 4px;
                        }
                        QPushButton:pressed {
                            background-color: #1abc9c;
                        }
                    """)
                else:
                    button.setStyleSheet("""
                        QPushButton {
                            background-color: #2c3e50;
                            color: white;
                            border-radius: 10px;
                            font-size: 16px;
                            padding: 8px;
                            margin: 4px;
                        }
                        QPushButton:pressed {
                            background-color: #16a085;
                        }
                    """)

                button.clicked.connect(lambda _, k=key: self.key_pressed(k))

                if key == 'Space':
                    self.grid.addWidget(button, row, col, 1, 6)
                    col += 6
                elif key in ['Backspace', 'Enter', 'Caps', 'Done']:
                    self.grid.addWidget(button, row, col, 1, 2)
                    col += 2
                else:
                    self.grid.addWidget(button, row, col)
                    col += 1
            row += 1

        self.setLayout(layout)

    def key_pressed(self, key):
        if not self.input_target:
            return

        current_text = self.input_target.text()

        if key == 'Backspace':
            self.input_target.setText(current_text[:-1])
        elif key == 'Enter':
            self.input_target.clearFocus()
            self.hide()
        elif key == 'Space':
            self.input_target.setText(current_text + ' ')
        elif key == 'Caps':
            self.caps_lock = not self.caps_lock
        elif key == 'Done':
            self.hide()
        else:
            char = key.upper() if self.caps_lock and len(key) == 1 else key
            self.input_target.setText(current_text + char)

        self.input_target.setCursorPosition(len(self.input_target.text()))


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

        top_bar = QHBoxLayout()
        logo_label = QLabel()
        pixmap = QPixmap("Images/image__1_-removebg-preview.png")
        logo_label.setPixmap(pixmap)
        logo_label.setFixedSize(160, 80)
        logo_label.setScaledContents(True)
        logo_label.setStyleSheet("background: transparent;")
        top_bar.addWidget(logo_label)
        top_bar.addStretch()
        support_button = QPushButton("Support")
        support_button.setFixedSize(100, 40)
        top_bar.addWidget(support_button)

        login_layout = QVBoxLayout()
        login_layout.setSpacing(10)
        login_layout.setAlignment(Qt.AlignCenter)

        username_label = QLabel("PATIENT ID:")
        username_label.setStyleSheet("color: white; font-size: 18px;")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your PATIENT ID")
        self.username_input.setFixedWidth(300)
        self.username_input.setStyleSheet("""
            padding: 10px;
            font-size: 18px;
            background-color: rgba(255, 255, 255, 0);
            color: white;
            border: none;
            border-bottom: 2px solid white;
        """)

        # password_label = QLabel("Password:")
        # password_label.setStyleSheet("color: white; font-size: 18px;")
        # self.password_input = QLineEdit()
        # self.password_input.setPlaceholderText("Enter your password")
        # self.password_input.setEchoMode(QLineEdit.Password)
        # self.password_input.setFixedWidth(300)
        # self.password_input.setStyleSheet("""
        #     padding: 10px;
        #     font-size: 18px;
        #     background-color: rgba(255, 255, 255, 0);
        #     color: white;
        #     border: none;
        #     border-bottom: 2px solid white;
        # """)

        login_button = QPushButton("Login")
        login_button.setFixedWidth(150)
        login_button.setFixedHeight(40)

        login_layout.addWidget(username_label)
        login_layout.addWidget(self.username_input)
        # login_layout.addWidget(password_label)
        # login_layout.addWidget(self.password_input)
        login_layout.addWidget(login_button, alignment=Qt.AlignCenter)

        bottom_bar = QHBoxLayout()
        power_button = QPushButton("Power Off")
        power_button.setFixedSize(120, 40)
        bottom_bar.addWidget(power_button)
        bottom_bar.addStretch()

        self.keyboard = VirtualKeyboard()
        main_layout.addLayout(top_bar)
        main_layout.addLayout(login_layout, stretch=1)
        main_layout.addWidget(self.keyboard)
        main_layout.addLayout(bottom_bar)

        self.keyboard.hide()
        self.username_input.installEventFilter(self)
        # self.password_input.installEventFilter(self)

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