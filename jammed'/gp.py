import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, 
    QVBoxLayout, QHBoxLayout, QWidget, QTableWidget, 
    QTableWidgetItem, QHeaderView, QAbstractItemView
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

class RobotDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Medical Robot Dashboard")
        self.showFullScreen()

        # Set background image
        selected_image = "./images/3f879af94e037b6ee67e2193cdbb436d 1.png"  
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Background label
        bg_label = QLabel(central_widget)
        bg_label.setPixmap(QPixmap(selected_image))
        bg_label.setScaledContents(True)
        bg_label.setGeometry(0, 0, self.width(), self.height())

        # Canvas for the table
        canvas = QWidget(central_widget)
        canvas.setStyleSheet("background-color: rgba(255, 255, 255, 180); border-radius: 15px;")
        canvas.setFixedSize(int(self.width() * 0.6), int(self.height() * 0.6))
        canvas.move(int(self.width() * 0.2), int(self.height() * 0.2))

        # Layout for canvas
        main_layout = QVBoxLayout(canvas)

        # Inventory Table Title
        title_label = QLabel("Inventory Table")
        title_label.setStyleSheet("font-size: 28px; font-weight: bold; padding: 10px;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # Table Widget (4 Rows, 5 Columns)
        self.table = QTableWidget(4, 5)
        self.table.setHorizontalHeaderLabels(["Room No.", "Bed No.", "Patient ID", "Referred By", "Medicine Attached"])

        # Stretch columns AND rows
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # Stretch columns
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)  # Stretch rows

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
        
        # Add Back Button
        self.back_button = QPushButton("Back", central_widget)
        self.back_button.setStyleSheet("font-size: 18px; padding: 10px; border-radius: 10px; background-color: #555; color: white;")
        self.back_button.setGeometry(20, self.height() - 60, 100, 40)
        self.back_button.clicked.connect(self.close)
        
        # Add Power Off Button
        self.power_off_button = QPushButton("Power Off", central_widget)
        self.power_off_button.setStyleSheet("font-size: 18px; padding: 10px; border-radius: 10px; background-color: red; color: white;")
        self.power_off_button.setGeometry(self.width() - 120, self.height() - 60, 100, 40)
        self.power_off_button.clicked.connect(self.close)  # Exits the application when clicked

        # Make rows and columns BIGGER for touch input
        self.table.setFont(QFont("Arial", 18))  # Bigger font
        self.table.setStyleSheet("QTableWidget::item { padding: 20px; }")  # Extra padding
        self.table.verticalHeader().setVisible(False)  # Hide row numbers
        self.table.setEditTriggers(QAbstractItemView.AllEditTriggers)  # Allow cell editing

        # Connect cell change event
        self.table.cellChanged.connect(self.check_and_add_buttons)

        main_layout.addWidget(self.table, 1)  # Expands table in height

        # Save Button (Right-Aligned)
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        save_button = QPushButton("Save")
        save_button.setStyleSheet("font-size: 20px; padding: 15px; border-radius: 10px; background-color: green; color: white;")
        save_button.clicked.connect(self.save_data)
        button_layout.addWidget(save_button)
        main_layout.addLayout(button_layout)

        self.show()

    def check_and_add_buttons(self, row, col):
        """Checks if first 4 columns are filled, then adds the button in the last column"""
        for i in range(4):  # Check first 4 columns
            if not self.table.item(row, i) or self.table.item(row, i).text().strip() == "":
                return  # If any cell is empty, exit

        # All first 4 columns have data, add "Attach Medicine" button
        attach_button = QPushButton("Attach Medicine")
        attach_button.setStyleSheet("font-size: 16px; padding: 10px; border-radius: 8px; background-color: blue; color: white;")
        attach_button.clicked.connect(lambda: self.attach_medicine(row))

        self.table.setCellWidget(row, 4, attach_button)

    def attach_medicine(self, row):
        """Function to handle the 'Attach Medicine' button click"""
        print(f"Medicine attached for Row {row + 1}")

    def save_data(self):
        print("Inventory Table data saved!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RobotDashboard()
    sys.exit(app.exec_())
