# Droid_GUI
 
hi this is abhinav

hello baby
hi abhinav


**add this in the login page** <br>
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QStackedWidget
from PyQt5.QtCore import Qt

# Import individual page modules
from login import LoginPage
from Nurse_dashboard import NurseDashboard
from admin_dashboard import AdminDashboard

class MainController(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize the stacked widget to manage pages
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Initialize pages
        self.login_page = LoginPage()
        self.nurse_dashboard = NurseDashboard()
        self.admin_dashboard = AdminDashboard()

        # Connect signals for navigation
        self.login_page.login_success.connect(self.handle_login)
        self.nurse_dashboard.logout_signal.connect(self.show_login)
        self.admin_dashboard.logout_signal.connect(self.show_login)

        # Add pages to the stack
        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.nurse_dashboard)
        self.stacked_widget.addWidget(self.admin_dashboard)

        # Show login page initially
        self.stacked_widget.setCurrentWidget(self.login_page)

    def handle_login(self, role):
        if role == "nurse":
            self.stacked_widget.setCurrentWidget(self.nurse_dashboard)
        elif role == "admin":
            self.stacked_widget.setCurrentWidget(self.admin_dashboard)
        else:
            self.show_login()

    def show_login(self):
        self.stacked_widget.setCurrentWidget(self.login_page)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainController()
    main_window.setWindowTitle("Application Flow")
    main_window.resize(800, 600)
    main_window.show()
    sys.exit(app.exec_())
