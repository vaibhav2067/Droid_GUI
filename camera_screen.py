import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtCore import QTimer, QSize

class CameraScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Camera Interface")
        self.showFullScreen()
        
        # Central Widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        
        # Background label
        bg_label = QLabel(central_widget)
        bg_label.setPixmap(QPixmap("./images/3f879af94e037b6ee67e2193cdbb436d 1.png"))
        bg_label.setScaledContents(True)
        bg_label.setGeometry(0, 0, self.width(), self.height())
        
        # Header Widget (same as main dashboard)
        header = QWidget(central_widget)
        header.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        header.setFixedHeight(100)
        header.setGeometry(0, 0, self.width(), 100)
        
        # Add logo to the header
        logo_label = QLabel(header)
        logo_label.setPixmap(QPixmap("./images/LOGO_edited_edited-removebg-preview.png"))
        logo_label.setScaledContents(True)
        logo_label.setGeometry(20, 20, 120, 60)
        
        # Add camera icon beside the logo
        camera_icon = QLabel(header)
        camera_icon.setPixmap(QPixmap("icons/Group 8.png"))
        camera_icon.setScaledContents(True)
        camera_icon.setGeometry(160, 22, 300, 50)

        # Add Back Button
        self.back_button = QPushButton("Back", central_widget)
        self.back_button.setStyleSheet("font-size: 18px; padding: 10px; border-radius: 10px; background-color: #555; color: white;")
        self.back_button.setGeometry(20, self.height() - 60, 100, 40)
        self.back_button.clicked.connect(self.close)

        #Power Off Button
        self.power_off_button = QPushButton("Power Off", central_widget)
        self.power_off_button.setStyleSheet("font-size: 18px; padding: 10px; border-radius: 10px; background-color: red; color: white;")
        self.power_off_button.setGeometry(self.width() - 120, self.height() - 60, 100, 40)
        self.power_off_button.clicked.connect(self.close)
        
        # Main layout
        main_layout = QHBoxLayout()
        
        # Left column (Camera Feed)
        self.camera_label = QLabel()
        self.camera_label.setStyleSheet("background-color: black;")
        main_layout.addWidget(self.camera_label, 2)  # Camera feed takes 2/3 of the space
        
        # Right column (Control Panel)
        control_layout = QVBoxLayout()
        buttons = [
            ("Capture", "icons/capture.png"),
            ("Record", "icons/record.png"),
            ("Gallery", "icons/gallery.png"),
            ("Settings", "icons/settings.png"),
            ("Zoom In", "icons/zoom-in.png"),
            ("Zoom Out", "icons/zoom-out.png")
        ]
        
        for text, icon in buttons:
            btn = QPushButton(text)
            btn.setIcon(QIcon(icon))
            btn.setIconSize(QSize(24, 24))
            btn.setStyleSheet("font-size: 16px; padding: 10px; border-radius: 10px;")
            control_layout.addWidget(btn)
        
        main_layout.addLayout(control_layout, 1)  # Control panel takes 1/3 of the space
        
        # Container for the layout
        container = QWidget(central_widget)
        container.setLayout(main_layout)
        container.setGeometry(int(self.width() * 0.1), int(self.height() * 0.2), int(self.width() * 0.8), int(self.height() * 0.6))
        container.setStyleSheet("background-color: rgba(255, 255, 255, 180); border-radius: 15px;")
        
        # Camera setup
        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)
        
        self.show()
    
    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            qimg = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.camera_label.setPixmap(QPixmap.fromImage(qimg))
    
    def closeEvent(self, event):
        self.cap.release()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CameraScreen()
    sys.exit(app.exec_())
