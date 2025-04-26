import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel,
    QPushButton, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QFrame, QMessageBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer,  QPoint, QPropertyAnimation, QRect



class FullscreenApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.image_paths = [
            "Images/3f879af94e037b6ee67e2193cdbb436d 1.png",
            "Images/9070125.jpg",
            "Images/download2.jpeg"
        ]
        self.current_index = 0
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Fullscreen Slideshow Background")

        # --- Central container widget ---
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # --- Background image label ---
        self.background_label = QLabel(central_widget)
        self.background_label.setScaledContents(True)
        self.background_label.setGeometry(self.geometry())

        # --- Foreground layout ---
        overlay_layout = QVBoxLayout()
        overlay_layout.setContentsMargins(20, 20, 20, 20)
        overlay_layout.setSpacing(10)

        # --- Top Bar: Logo (left) + Login Button (right) ---
        top_bar = QHBoxLayout()

        # Logo
        logo_label = QLabel()
        pixmap = QPixmap("Images/LOGO_edited_edited-removebg-preview.png")
        logo_label.setPixmap(pixmap)
        logo_label.setFixedSize(200, 100)
        logo_label.setScaledContents(True)
        logo_label.setStyleSheet("background: transparent;")
        top_bar.addWidget(logo_label)

        top_bar.addStretch()

        # Login Button (top-right)
        login_button = QPushButton("Login")
        login_button.setFixedSize(120, 50)
        login_button.setStyleSheet("""font-size: 18px;
            background-color: #4CAF50;
            color: white;
            border-radius: 20px;""")
        top_bar.addWidget(login_button)

        overlay_layout.addLayout(top_bar)

        # --- Spacer in the middle ---
        overlay_layout.addStretch()

        # --- Bottom Controls ---
        bottom_bar = QHBoxLayout()

        # Left/right arrows in bottom-left
        arrow_layout = QHBoxLayout()

        self.left_button = QPushButton("◀", self.centralWidget())
        self.left_button.setFixedSize(80, 80)
        self.left_button.setStyleSheet("""font-size: 24px;
            background-color: #00FFFFFF;
            color: white;
            border-radius: 40px;""")
        self.left_button.clicked.connect(self.prev_image)

        self.right_button = QPushButton("▶", self.centralWidget())
        self.right_button.setFixedSize(80, 80)
        self.right_button.setStyleSheet("""font-size: 24px;
            background-color: #00FFFFFF;
            color: white;
            border-radius: 40px;""")
        self.right_button.clicked.connect(self.next_image)


        # arrow_layout.addWidget(left_button)
        # arrow_layout.addWidget(right_button)

        # bottom_bar.addLayout(arrow_layout)
        bottom_bar.addStretch()

        # Add this inside FullscreenApp class, after 'bottom_bar.addStretch()'
        self.get_started_slider = SliderWidget()
        bottom_bar.addWidget(self.get_started_slider)


        # "Get Started" slider/button in bottom-right
        # get_started_button = QPushButton("➤ Get Started")
        # get_started_button.setFixedSize(200, 60)
        # get_started_button.setStyleSheet("""
        #     font-size: 20px;
        #     background-color: #4CAF50;
        #     color: white;
        #     border-radius: 20px;
        # """)
        # bottom_bar.addWidget(get_started_button)

        overlay_layout.addLayout(bottom_bar)

        # Set layout
        central_widget.setLayout(overlay_layout)

        # Update and show background
        self.update_background()
        self.resizeEvent = self.on_resize

        # Auto slideshow
        timer = QTimer(self)
        timer.timeout.connect(self.next_image)
        timer.start(10000)

        self.showFullScreen()

    def on_resize(self, event):
        self.background_label.setGeometry(self.rect())
        self.update_background()

        # Position left/right arrow buttons in the vertical middle
        center_y = self.height() // 2 - 40  # 40 = half of button height

        self.left_button.move(20, center_y)
        self.right_button.move(self.width() - self.right_button.width() - 20, center_y)


    def update_background(self):
        if not self.image_paths:
            return
        path = self.image_paths[self.current_index]
        if os.path.exists(path):
            pixmap = QPixmap(path).scaled(
                self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
            )
            self.background_label.setPixmap(pixmap)

    def prev_image(self):
        self.current_index = (self.current_index - 1) % len(self.image_paths)
        self.update_background()

    def next_image(self):
        self.current_index = (self.current_index + 1) % len(self.image_paths)
        self.update_background()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

class SliderWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(300, 60)
        self.setStyleSheet("background-color: #ddd; border-radius: 30px;")
        self.setMouseTracking(True)

        # Slider button
        self.button = QLabel("Get Started →", self)
        self.button.setStyleSheet("""
            font-size: 16px;                      
            background-color: #4CAF50; color: white;
            border-radius: 25px; text-align: center;
        """)
        self.button.setAlignment(Qt.AlignCenter)
        self.button.setGeometry(0, 0, 140, 60)
        self.button.setAttribute(Qt.WA_TransparentForMouseEvents, True)

        self.dragging = False
        self.offset = QPoint()

    def mousePressEvent(self, event):
        if self.button.geometry().contains(event.pos()):
            self.dragging = True
            self.offset = event.pos() - self.button.pos()

    def mouseMoveEvent(self, event):
        if self.dragging:
            x = event.pos().x() - self.offset.x()
            x = max(0, min(x, self.width() - self.button.width()))
            self.button.move(x, 0)

    def mouseReleaseEvent(self, event):
        if self.dragging:
            self.dragging = False
            # Check if at end
            if self.button.x() >= self.width() - self.button.width() - 10:
                self.showPopup()
            self.resetSlider()

    def resetSlider(self):
        anim = QPropertyAnimation(self.button, b"geometry")
        anim.setDuration(300)
        anim.setStartValue(self.button.geometry())
        anim.setEndValue(QRect(0, 0, 140, 60))
        anim.start()
        self.anim = anim  # Keep reference alive

    def showPopup(self):
        msg = QMessageBox()
        msg.setWindowTitle("Success")
        msg.setText("Slider activated! 🎉")
        msg.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FullscreenApp()
    sys.exit(app.exec_())