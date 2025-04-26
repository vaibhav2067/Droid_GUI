import sys
import os
import socket
import platform
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QWidget,
    QHBoxLayout, QVBoxLayout, QFrame, QMessageBox
)
from PyQt5.QtGui import QPixmap, QPalette, QBrush
from PyQt5.QtCore import Qt, QTimer, QPoint, QPropertyAnimation, QRect, pyqtSignal

# ================== QSS Style Section ==================
QSS_STYLE = """
QMainWindow {
}

QPushButton {
    font-size: 16px;
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 8px;
}

QPushButton:hover {
    background-color: #2980b9;
}

QPushButton:pressed {
    background-color: #1c5980;
}

QLabel#CanvasLabel {
    background-color: #F6F4F1;
    border: 2px solid #ccc;
    border-radius: 20px;
}

SliderWidget {
    background-color: #ddd;
    border-radius: 30px;
}

SliderWidget QLabel {
    font-size: 16px;
    background-color: #4CAF50;
    color: white;
    border-radius: 25px;
    text-align: center;
}
"""

# ========== Utility: Check Internet Connection ==========
def is_connected():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except OSError:
        return False

def get_connected_network_name():
    try:
        system = platform.system()
        if system == "Windows":
            result = subprocess.check_output("netsh wlan show interfaces", shell=True).decode()
            for line in result.split("\n"):
                if "SSID" in line and "BSSID" not in line:
                    return line.split(":")[1].strip()
        elif system == "Linux":
            result = subprocess.check_output(
                "nmcli -t -f active,ssid dev wifi", shell=True
            ).decode()
            for line in result.splitlines():
                if line.startswith("yes:"):
                    return line.split(":")[1]
        else:
            return "Unsupported OS"
    except Exception as e:
        return f"Error: {e}"
    return "Not Connected"

# ========== Custom QLabel for Clickable Icon ==========
class ClickableLabel(QLabel):
    clicked = pyqtSignal()
    def mousePressEvent(self, event):
        self.clicked.emit()

# ================== Slider Widget ==================
class SliderWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(300, 60)
        self.setMouseTracking(True)

        self.button = QLabel("Get Started →", self)
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
            if self.button.x() >= self.width() - self.button.width() - 10:
                self.showPopup()
            self.resetSlider()

    def resetSlider(self):
        anim = QPropertyAnimation(self.button, b"geometry")
        anim.setDuration(300)
        anim.setStartValue(self.button.geometry())
        anim.setEndValue(QRect(0, 0, 140, 60))
        anim.start()
        self.anim = anim

    def showPopup(self):
        if hasattr(self.parent(), "current_mode"):
            try:
                if self.parent().current_mode == "vital":
                    subprocess.Popen([sys.executable, "screen_saver.py"])
                elif self.parent().current_mode == "inventory":
                    subprocess.Popen([sys.executable, "SCREENSAVER.py"])
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to launch: {e}")

# ================== Main Window ==================
class FullScreenWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.vital_images = [
            os.path.join(BASE_DIR, "Images/Slide_images/slide1_vital.jpg"),
            os.path.join(BASE_DIR, "Images/Slide_images/slide2_vital.jpg"),
            os.path.join(BASE_DIR, "Images/Slide_images/slide3_vital.jpg")
        ]
        self.inventory_images = [
            os.path.join(BASE_DIR, "Images/Slide_images/slide1_inventory.jpg"),
            os.path.join(BASE_DIR, "Images/Slide_images/slide2_vital.jpg"),
            os.path.join(BASE_DIR, "Images/Slide_images/slide3_vital.jpg")
        ]
        self.current_images = []
        self.image_index = 0
        self.current_mode = None

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_slideshow)

        self.initUI()

    def initUI(self):
        self.showFullScreen()
        self.setStyleSheet(QSS_STYLE)

        background_image = QPixmap("Images/background.jpg").scaled(
            self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation
        )
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(background_image))
        self.setPalette(palette)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Top Bar
        top_layout = QHBoxLayout()
        logo_label = QLabel()
        logo_pixmap = QPixmap("Images/logos/Logo.png").scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(logo_pixmap)
        top_layout.addWidget(logo_label, alignment=Qt.AlignLeft)
        top_layout.addStretch()

        # Wi-Fi Icon
        self.wifi_icon = ClickableLabel()
        self.wifi_icon.clicked.connect(self.show_wifi_info)
        self.update_wifi_icon()
        top_layout.addWidget(self.wifi_icon, alignment=Qt.AlignRight)

        # Timer to refresh icon
        self.network_timer = QTimer()
        self.network_timer.timeout.connect(self.update_wifi_icon)
        self.network_timer.start(10000)

        # Support Button
        support_button = QPushButton("Support")
        support_button.setFixedSize(100, 40)
        support_button.clicked.connect(lambda: QMessageBox.information(self, "Support", "Support feature coming soon."))
        top_layout.addWidget(support_button, alignment=Qt.AlignRight)

        main_layout.addLayout(top_layout)

        # Split layout
        split_layout = QHBoxLayout()

        # Left Panel
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_layout.addStretch()

        self.vital_button = QPushButton("Vital Monitor")
        self.inventory_button = QPushButton("Inventory")

        for btn in (self.vital_button, self.inventory_button):
            btn.setFixedSize(200, 60)
            left_layout.addWidget(btn, alignment=Qt.AlignHCenter)
            left_layout.addSpacing(20)

        left_layout.addStretch()
        left_widget.setLayout(left_layout)
        split_layout.addWidget(left_widget, stretch=1)

        self.vital_button.clicked.connect(self.start_vital_slideshow)
        self.inventory_button.clicked.connect(self.start_inventory_slideshow)

        # Right Panel (Canvas)
        canvas_container = QWidget()
        canvas_vbox = QVBoxLayout()
        canvas_vbox.addStretch()

        self.canvas_label = QLabel()
        self.canvas_label.setObjectName("CanvasLabel")
        self.canvas_label.setFixedSize(700, 460)
        self.canvas_label.setAlignment(Qt.AlignCenter)
        canvas_vbox.addWidget(self.canvas_label)

        canvas_vbox.addStretch()
        canvas_container.setLayout(canvas_vbox)
        split_layout.addWidget(canvas_container, stretch=1)

        main_layout.addLayout(split_layout)

        # Bottom Layout
        bottom_layout = QHBoxLayout()

        # Power Button
        power_button = QPushButton("Power Off")
        power_button.setFixedSize(100, 40)
        power_button.clicked.connect(self.confirm_exit)
        bottom_layout.addWidget(power_button, alignment=Qt.AlignLeft)
        bottom_layout.addStretch()

        # Slider
        self.slider = SliderWidget(self)
        self.slider.setVisible(False)
        slider_wrapper = QWidget()
        slider_wrapper.setFixedSize(300, 60)
        slider_layout = QHBoxLayout()
        slider_layout.setContentsMargins(0, 0, 0, 0)
        slider_layout.addWidget(self.slider)
        slider_wrapper.setLayout(slider_layout)
        bottom_layout.addWidget(slider_wrapper, alignment=Qt.AlignRight)

        main_layout.addLayout(bottom_layout)

    def update_wifi_icon(self):
        icon_file = "wifi_connected.png" if is_connected() else "wifi_disconnected.png"
        icon_path = os.path.join("Images", "icons", icon_file)

        if not os.path.exists(icon_path):
            print(f"⚠ Wi-Fi icon not found: {icon_path}")
            self.wifi_icon.clear()
            return

        pixmap = QPixmap(icon_path)
        if pixmap.isNull():
            print(f"⚠ Failed to load pixmap: {icon_path}")
            self.wifi_icon.clear()
        else:
            self.wifi_icon.setPixmap(pixmap.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation))


    def show_wifi_info(self):
        network_name = get_connected_network_name()

        popup = QWidget(self)
        popup.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup)
        popup.setStyleSheet("""
            background-color: white;
            border: 2px solid #ccc;
            border-radius: 10px;
            padding: 10px;
            font-size: 12px;
        """)
        label = QLabel(network_name, popup)
        layout = QVBoxLayout()
        layout.addWidget(label)
        popup.setLayout(layout)

        # Position under icon
        global_pos = self.wifi_icon.mapToGlobal(QPoint(0, self.wifi_icon.height()))
        popup.move(global_pos)
        popup.adjustSize()
        popup.show()

        QTimer.singleShot(5000, popup.close)

    def confirm_exit(self):
        msg = QMessageBox(self)
        msg.setText("⚠ You are Logging Out. Do you want to continue?")
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Cancel)
        msg.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #fefefe;
                border: 2px solid #ccc;
                border-radius: 15px;
                font-size: 16px;
            }
            QPushButton {
                min-width: 80px;
                padding: 6px;
                border-radius: 8px;
                background-color: #3498db;
                color: white;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1c5980;
            }
        """)
        result = msg.exec_()
        if result == QMessageBox.Yes:
            QApplication.quit()

    def start_vital_slideshow(self):
        self.current_mode = "vital"
        self.slider.setVisible(True)
        self.start_slideshow(self.vital_images)

    def start_inventory_slideshow(self):
        self.current_mode = "inventory"
        self.slider.setVisible(True)
        self.start_slideshow(self.inventory_images)

    def start_slideshow(self, images):
        self.current_images = [img for img in images if os.path.exists(img)]
        if not self.current_images:
            self.canvas_label.setText("No images found.")
            self.timer.stop()
            return
        self.image_index = 0
        self.update_slideshow()
        self.timer.start(3000)

    def update_slideshow(self):
        if not self.current_images:
            return
        image_path = self.current_images[self.image_index]
        pixmap = QPixmap(image_path).scaled(
            self.canvas_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.canvas_label.setPixmap(pixmap)
        self.image_index = (self.image_index + 1) % len(self.current_images)

# ================== Run App ==================
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FullScreenWindow()
    window.show()
    sys.exit(app.exec_())