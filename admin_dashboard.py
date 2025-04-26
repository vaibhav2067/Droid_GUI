import sys
import os
import socket
import platform
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QWidget,
    QHBoxLayout, QVBoxLayout, QFrame, QMessageBox, QLineEdit, QListWidget, QListWidgetItem
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

# ========== Get Wi-Fi Networks (Linux) ==========

def get_wifi_networks_linux():
    try:
        result = subprocess.check_output("nmcli -t -f active,ssid,signal dev wifi", shell=True).decode()
        networks = []
        current_ssid = None

        for line in result.strip().split("\n"):
            parts = line.strip().split(":")
            if len(parts) < 3:
                continue
            active, ssid, signal = parts
            networks.append((ssid, signal, active == "yes"))
            if active == "yes":
                current_ssid = ssid
        return current_ssid, networks
    except Exception as e:
        return None, []

# ========== Get Wi-Fi Networks (macOS) ==========

def get_wifi_networks_mac():
    try:
        result = subprocess.check_output("airport -s", shell=True).decode()
        networks = []
        current_ssid = None

        for line in result.strip().split("\n"):
            if line.startswith("SSID"):
                continue
            parts = line.strip().split()
            if len(parts) < 3:
                continue
            ssid, signal = parts[0], parts[2]
            networks.append((ssid, signal, False))  # macOS doesn't show active status here
        return current_ssid, networks
    except Exception as e:
        return None, []

# ========== Get Wi-Fi Networks (Windows) ==========

def get_wifi_networks_windows():
    try:
        result = subprocess.check_output("netsh wlan show networks mode=Bssid", shell=True).decode()
        networks = []
        current_ssid = None

        for line in result.strip().split("\n"):
            if "SSID" in line:
                ssid = line.split(":")[1].strip()
                networks.append((ssid, "N/A", False))  # Windows doesn't show signal strength easily
        return current_ssid, networks
    except Exception as e:
        return None, []

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
        current_ssid, networks = None, []

        if platform.system() == "Linux":
            current_ssid, networks = get_wifi_networks_linux()
        elif platform.system() == "Darwin":  # macOS
            current_ssid, networks = get_wifi_networks_mac()
        elif platform.system() == "Windows":
            current_ssid, networks = get_wifi_networks_windows()

        popup = QWidget(self)
        popup.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup)
        popup.setStyleSheet("""
            background-color: white;
            border: 2px solid #ccc;
            border-radius: 10px;
            font-size: 14px;
            padding: 10px;
        """)

        layout = QVBoxLayout()
        title = QLabel(f"Connected to: {current_ssid if current_ssid else 'None'}")
        layout.addWidget(title)

        list_widget = QListWidget()
        for ssid, signal, is_active in networks:
            item = QListWidgetItem(f"{ssid} ({signal}%)")
            if is_active:
                item.setBackground(Qt.lightGray)
            list_widget.addItem(item)

        def on_item_clicked(item):
            selected_ssid = item.text().split(" (")[0]
            QMessageBox.information(popup, "Wi-Fi", f"Connecting to {selected_ssid}...")
            # Here you would implement the logic to connect to the selected network

        list_widget.itemClicked.connect(on_item_clicked)
        layout.addWidget(list_widget)

        popup.setLayout(layout)
        popup.show()
