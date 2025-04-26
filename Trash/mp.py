import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QGridLayout, QWidget
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize, QTimer, QPropertyAnimation
from PyQt5.QtWidgets import QGraphicsOpacityEffect

class RobotDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.update_background()  # Load first image
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_background)
        self.timer.start(10000)  # Update every 30 seconds

    def initUI(self):
        self.setWindowTitle("Medical Robot Dashboard")
        self.showFullScreen()

        # Central Widget for the background
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Background label for the central widget
        self.bg_label = QLabel(self.central_widget)
        self.bg_label.setScaledContents(True)
        self.bg_label.setGeometry(0, 0, self.width(), self.height())

        # Opacity Effect for smooth transition
        self.opacity_effect = QGraphicsOpacityEffect()
        self.bg_label.setGraphicsEffect(self.opacity_effect)

        # Header Widget (to hold the logo)
        header = QWidget(self.central_widget)
        header.setStyleSheet("background-color: rgba(0, 0, 0, 0);")  
        header.setFixedHeight(100)
        header.setGeometry(0, 0, self.width(), 100)

        # Add the logo
        logo_label = QLabel(header)
        logo_label.setPixmap(QPixmap("./images/LOGO_edited_edited-removebg-preview.png"))
        logo_label.setScaledContents(True)
        logo_label.setGeometry(20, 20, 120, 60)

        # Canvas Widget (Smaller than Full Screen)
        canvas = QWidget(self.central_widget)
        canvas.setStyleSheet("background-color: rgba(255, 255, 255, 180); border-radius: 15px;")
        canvas.setFixedSize(int(self.width() * 0.6), int(self.height() * 0.6))
        canvas.move(int(self.width() * 0.2), int(self.height() * 0.2))

        # Grid Layout for Buttons
        grid_layout = QGridLayout()

        # Creating Buttons with Icons
        buttons = {
            "Inventory Table": ("icons/clarity--table-line.png", "  Inventory Table"),
            "Vital Monitoring": ("icons/mdi--clipboard-vitals-outline.png", "  Vital Monitoring"),
            "Manual Control": ("icons/game-icons--mechanical-arm.png", "  Manual Robot Control"),
            "Camera": ("icons/tdesign--camera-2.png", "  Camera")
        }

        row, col = 0, 0
        for _, (icon_path, text) in buttons.items():
            btn = QPushButton(text)
            btn.setIcon(QIcon(icon_path))
            btn.setIconSize(QSize(20, 20))
            btn.setStyleSheet("font-size: 18px; padding: 15px; border-radius: 10px;")
            grid_layout.addWidget(btn, row, col)
            col += 1
            if col > 1:
                col = 0
                row += 1

        # Set layout for the canvas
        layout_widget = QWidget(canvas)
        layout_widget.setLayout(grid_layout)
        layout_widget.setGeometry(20, 20, canvas.width() - 40, canvas.height() - 40)

        self.show()

    def update_background(self):
        """Fetches a random image, updates the background with a fade-in effect."""
        try:
            img_url = "https://picsum.photos/1920/1080"  # Random image API
            response = requests.get(img_url, stream=True)

            if response.status_code == 200:
                with open("background.jpg", "wb") as f:
                    f.write(response.content)

                # Apply transition effect
                self.start_fade_animation()
        except Exception as e:
            print(f"Error fetching image: {e}")

    def start_fade_animation(self):
        """Creates a fade-in effect when changing the background."""
        self.opacity_effect.setOpacity(0)  # Start with transparent
        self.bg_label.setPixmap(QPixmap("background.jpg"))  # Load new image

        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(1500)  # 1.5 seconds fade-in duration
        self.animation.setStartValue(0)  # Start from transparent
        self.animation.setEndValue(1)  # Fully visible
        self.animation.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RobotDashboard()
    sys.exit(app.exec_())
