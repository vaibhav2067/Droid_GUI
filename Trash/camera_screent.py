import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFrame, QListWidget, QSizePolicy, QSlider
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from live_wallpaper import LiveWallpaperWidget  # Import the live wallpaper

class CameraScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.live_wallpaper = None  # Define it before UI initialization
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Camera Interface")
        self.showFullScreen()

        # Central Widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Live Wallpaper Background
        self.live_wallpaper = LiveWallpaperWidget(central_widget)
        self.live_wallpaper.setGeometry(0, 0, self.width(), self.height())  # Set geometry immediately (as in crouch.py)
        self.live_wallpaper.lower()  # Keep it in the background

        # Main Layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Header (Logo & Title)
        header = QWidget()
        header_layout = QHBoxLayout()
        header.setLayout(header_layout)
        header.setFixedHeight(100)
        header.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        
        logo_label = QLabel()
        logo_label.setPixmap(QPixmap("./images/LOGO_edited_edited-removebg-preview.png"))
        logo_label.setScaledContents(True)
        logo_label.setFixedSize(120, 60)
        
        title_label = QLabel("Camera Interface")
        title_label.setStyleSheet("font-size: 24px; color: white;")
        title_label.setAlignment(Qt.AlignCenter)
        
        header_layout.addWidget(logo_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        # Camera Feed Area
        camera_frame = QLabel("Camera Feed")
        camera_frame.setStyleSheet("background-color: black; border-radius: 10px; color: white;")
        camera_frame.setAlignment(Qt.AlignCenter)
        camera_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Control Panel (Buttons)
        control_panel = QWidget()
        control_layout = QHBoxLayout()
        control_panel.setLayout(control_layout)
        control_panel.setFixedHeight(80)
        
        capture_btn = QPushButton("Capture 🖼️")
        record_btn = QPushButton("Record 🎥")
        toggle_camera_btn = QPushButton("Toggle Camera 🔄")
        zoom_slider = QSlider(Qt.Horizontal)
        zoom_slider.setMinimum(1)
        zoom_slider.setMaximum(10)
        zoom_slider.setValue(5)

        control_layout.addWidget(capture_btn)
        control_layout.addWidget(record_btn)
        control_layout.addWidget(toggle_camera_btn)
        control_layout.addWidget(zoom_slider)

        # Sidebar (Gallery & Settings)
        sidebar = QFrame()
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet("background-color: rgba(255, 255, 255, 180); border-radius: 10px;")
        sidebar_layout = QVBoxLayout()
        sidebar.setLayout(sidebar_layout)
        
        snapshot_gallery = QListWidget()
        snapshot_gallery.setFixedHeight(300)
        snapshot_gallery.addItem("Captured Images")
        
        settings_btn = QPushButton("Settings ⚙️")
        
        sidebar_layout.addWidget(snapshot_gallery)
        sidebar_layout.addWidget(settings_btn)

        # Bottom Panel (Back Button)
        back_button = QPushButton("⬅ Back")
        back_button.setStyleSheet("font-size: 18px; padding: 10px;")
        back_button.clicked.connect(self.go_back)

        # Layout Management
        content_layout = QHBoxLayout()
        content_layout.addWidget(camera_frame, 2)
        content_layout.addWidget(sidebar, 1)
        
        main_layout.addWidget(header)
        main_layout.addLayout(content_layout)
        main_layout.addWidget(control_panel)
        main_layout.addWidget(back_button)

        # Ensure live wallpaper resizes correctly
        self.resizeEvent(None)  # 🔹 Forces resizing

    def resizeEvent(self, event):
        """Ensure live wallpaper resizes correctly when window resizes."""
        if self.live_wallpaper:
            self.live_wallpaper.setGeometry(0, 0, self.width(), self.height())  # Full screen size
            self.live_wallpaper.update()  # 🔹 Force repaint
        super().resizeEvent(event)

    def go_back(self):
        from Trash.crouch import RobotDashboard  # Import your main dashboard file
        self.new_window = RobotDashboard()
        self.new_window.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CameraScreen()
    window.show()
    sys.exit(app.exec_())