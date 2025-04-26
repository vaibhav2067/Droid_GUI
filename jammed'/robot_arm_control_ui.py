import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QGridLayout, QWidget, QSlider
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl


class RobotArmControl(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Robot Arm Control")
        self.showFullScreen()

        selected_image = "./images/3f879af94e037b6ee67e2193cdbb436d 1.png"

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        bg_label = QLabel(central_widget)
        bg_label.setPixmap(QPixmap(selected_image))
        bg_label.setScaledContents(True)
        bg_label.setGeometry(0, 0, self.width(), self.height())

        header = QWidget(central_widget)
        header.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        header.setFixedHeight(100)
        header.setGeometry(0, 0, self.width(), 100)

        logo_label = QLabel(header)
        logo_label.setPixmap(QPixmap("./images/LOGO_edited_edited-removebg-preview.png"))
        logo_label.setScaledContents(True)
        logo_label.setGeometry(20, 20, 120, 60)

        self.power_off_button = QPushButton("Power Off", central_widget)
        self.power_off_button.setStyleSheet("font-size: 18px; padding: 10px; border-radius: 10px; background-color: red; color: white;")
        self.power_off_button.setGeometry(self.width() - 120, self.height() - 60, 100, 40)
        self.power_off_button.clicked.connect(self.close)

        main_layout = QGridLayout()
        content_widget = QWidget(central_widget)
        content_widget.setLayout(main_layout)
        content_widget.setGeometry(50, 120, self.width() - 100, self.height() - 170)

        # First Column - Embedded Web 3D Model Viewer
        self.web_view = QWebEngineView()
        self.web_view.setUrl(QUrl.fromUserInput("https://skfb.ly/6RMEN"))  # Replace with a proper 3D model link
        self.web_view.setFixedSize(int(self.width() * 0.45), int(self.height() * 0.7))

        # Second Column - Control Panel
        control_panel = QWidget()
        control_layout = QVBoxLayout()
        control_panel.setLayout(control_layout)
        control_panel.setStyleSheet("background-color: rgba(255, 255, 255, 180); border-radius: 15px;")
        control_panel.setFixedSize(int(self.width() * 0.45), int(self.height() * 0.7))

        # Sliders for four joints with better styling
        joints = ["Grip Joint", "First Hinge", "Elbow Joint", "Arm Joint"]
        for joint in joints:
            slider_label = QLabel(f"{joint} Angle")
            slider_label.setStyleSheet("font-size: 16px; font-weight: bold; padding: 5px;")
            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(0)
            slider.setMaximum(180)
            slider.setValue(90)
            slider.setStyleSheet("QSlider::groove:horizontal { height: 8px; background: lightgray; border-radius: 4px; }"
                                 "QSlider::handle:horizontal { background: blue; width: 18px; height: 18px; border-radius: 9px; margin: -5px 0; }")
            control_layout.addWidget(slider_label)
            control_layout.addWidget(slider)

        main_layout.addWidget(self.web_view, 0, 0)
        main_layout.addWidget(control_panel, 0, 1)
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RobotArmControl()
    sys.exit(app.exec_())
