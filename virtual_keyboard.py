# virtual_keyboard.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QSizePolicy
from PyQt5.QtCore import Qt


class VirtualKeyboard(QWidget):
    def __init__(self, input_target=None):  # input_target is OPTIONAL
        super().__init__()
        self.input_target = input_target
        self.caps_lock = False
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.setAlignment(Qt.AlignCenter)

        self.grid = QGridLayout()
        hbox.addLayout(self.grid)
        layout.addLayout(hbox)

        self.keys = [
            ['~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '\''],
            ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'Backspace'],
            ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', ';'],
            ['Caps', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'Enter'],
            ['Done', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', '\\'],
            ['Space']
        ]

        row = 0
        for key_row in self.keys:
            col = 0
            for key in key_row:
                button = QPushButton(key)
                button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                button.clicked.connect(lambda _, k=key: self.key_pressed(k))

                if key == 'Space':
                    self.grid.addWidget(QWidget(), row, col, 1, 2)
                    col += 4
                    self.grid.addWidget(button, row, col, 1, 6)
                    col += 6
                    self.grid.addWidget(QWidget(), row, col, 1, 2)
                    col += 2
                elif key in ['Backspace', 'Enter', 'Caps', 'Done']:
                    self.grid.addWidget(button, row, col, 1, 2)
                    col += 2
                else:
                    self.grid.addWidget(button, row, col)
                    col += 1
            row += 1

        self.setLayout(layout)
        self.apply_styles()

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
            self.update_caps_lock()
        elif key == 'Done':
            self.hide()
        else:
            char = key.upper() if self.caps_lock else key.lower()
            self.input_target.setText(current_text + char)

        self.input_target.setCursorPosition(len(self.input_target.text()))

    def update_caps_lock(self):
        for i in range(self.grid.count()):
            item = self.grid.itemAt(i).widget()
            if isinstance(item, QPushButton):
                text = item.text()
                if len(text) == 1 and text.isalpha():
                    item.setText(text.upper() if self.caps_lock else text.lower())

    def apply_styles(self):
        self.setStyleSheet("""
            QPushButton {
                background-color: #2c3e50;
                color: white;
                border-radius: 10px;
                font-size: 18px;
                padding: 10px;
                margin: 4px;
            }
            QPushButton:pressed {
                background-color: #16a085;
            }
        """)
