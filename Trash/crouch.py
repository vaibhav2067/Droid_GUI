import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QGridLayout, QWidget
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize
from Trash.camera_screen import CameraScreen
from live_wallpaper import LiveWallpaperWidget


class RobotDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Medical Robot Dashboard")
        self.showFullScreen()  # Set the window to full screen

        # Central Widget for the background
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        central_widget.setGeometry(0, 0, self.width(), self.height())

        # Live Wallpaper (Matplotlib Animation) – Set it to fill the entire window
        live_wallpaper = LiveWallpaperWidget(central_widget)
        live_wallpaper.setGeometry(0, 0, self.width(), self.height())  # Full screen size

        # Header Widget (to hold the logo)
        header = QWidget(central_widget)
        header.setStyleSheet("background-color: rgba(0, 0, 0, 0);")  # Dark semi-transparent background
        header.setFixedHeight(100)  # Height of the header
        header.setGeometry(0, 0, self.width(), 100)

        # Add the logo to the header (replace "logo_path.png" with your image path)
        logo_label = QLabel(header)
        logo_label.setPixmap(QPixmap("./images/LOGO_edited_edited-removebg-preview.png"))  # Replace with your logo image
        logo_label.setScaledContents(True)
        logo_label.setGeometry(20, 20, 120, 60)  # Positioning and size of the logo

        # Canvas Widget (Smaller than Full Screen)
        canvas = QWidget(central_widget)
        canvas.setStyleSheet("background-color: rgba(255, 255, 255, 180); border-radius: 15px;")
        canvas.setFixedSize(int(self.width() * 0.6), int(self.height() * 0.6))
        canvas.move(int(self.width() * 0.2), int(self.height() * 0.2))

        # Grid Layout for Buttons
        grid_layout = QGridLayout()



        # Creating Buttons with Icons
        buttons = {
            "Inventory Table": ("icons/clarity--table-line.png", "  Inventory Table"),  # Replace with your icons
            "Vital Monitoring": ("icons/mdi--clipboard-vitals-outline.png", "  Vital Monitoring"),    # Replace with your icons
            "Manual Control": ("icons/game-icons--mechanical-arm.png", "  Manual Robot Control"), # Replace with your icons
            "Camera": ("icons/tdesign--camera-2.png", "  Camera")                        # Replace with your icons
        }

        row, col = 0, 0
        for btn_text, (icon_path, text) in buttons.items():
            btn = QPushButton(text)
            btn.setIcon(QIcon(icon_path))  # Set the icon
            btn.setIconSize(QSize(20, 20))  # Set the icon size
            btn.setStyleSheet("font-size: 18px; padding: 15px; border-radius: 10px; background-color: rgba(255, 255, 255, 255)")
            btn.clicked.connect(self.open_camera_screen)
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

    def open_camera_screen(self):
            self.camera_window = CameraScreen()  # Create CameraScreen instance
            self.camera_window.show()
            self.close()  # Close the main dashboard (optional)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RobotDashboard()
    sys.exit(app.exec_())
