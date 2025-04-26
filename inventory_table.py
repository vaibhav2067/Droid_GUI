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

        selected_image = "Images/background.jpg" # Add you Background img as per your requirements 
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.bg_label = QLabel(self.central_widget)
        self.bg_label.setPixmap(QPixmap(selected_image))
        self.bg_label.setScaledContents(True)
        self.bg_label.setGeometry(0, 0, self.width(), self.height())

        self.canvas = QWidget(self.central_widget)
        self.canvas.setStyleSheet("background-color: rgba(255, 255, 255, 180); border-radius: 15px; border: 1px solid #ccc")
        self.canvas.setFixedSize(int(self.width() * 0.6), int(self.height() * 0.6))
        self.canvas.move(int(self.width() * 0.2), int(self.height() * 0.2))
        self.canvas_layout = QVBoxLayout(self.canvas)

        header = QWidget(self.central_widget)
        header.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        header.setFixedHeight(100)
        header.setGeometry(0, 0, self.width(), 100)

        logo_label = QLabel(header)
        logo_label.setPixmap(QPixmap("Images/logos/Logo.png")) # Add Logo, you guys are comfortable with.
        logo_label.setScaledContents(True)
        logo_label.setGeometry(20, 20, 120, 60)

        self.back_button = QPushButton("Back", self.central_widget)
        self.back_button.setStyleSheet("font-size: 18px; padding: 10px; border-radius: 10px; background-color: #555; color: white;")
        self.back_button.setGeometry(20, self.height() - 60, 100, 40)
        self.back_button.clicked.connect(self.close)

        self.power_off_button = QPushButton("Power Off", self.central_widget)
        self.power_off_button.setStyleSheet("font-size: 18px; padding: 10px; border-radius: 10px; background-color: red; color: white;")
        self.power_off_button.setGeometry(self.width() - 120, self.height() - 60, 100, 40)
        self.power_off_button.clicked.connect(self.close)

        self.create_inventory_table()

    def create_inventory_table(self):
        self.clear_layout(self.canvas_layout)

        title_label = QLabel("Inventory Table")
        title_label.setStyleSheet("font-size: 28px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignCenter)
        self.canvas_layout.addWidget(title_label)

        self.table = QTableWidget(4, 5)
        self.table.setHorizontalHeaderLabels(["Room No.", "Bed No.", "Patient ID", "Referred By", "Medicine Attached"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.table.setFont(QFont("Arial", 18))
        self.table.setStyleSheet("QTableWidget::item { padding: 20px; }")
        self.table.cellChanged.connect(self.check_and_add_buttons)

        self.canvas_layout.addWidget(self.table)

        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()

        save_button = QPushButton("Save")
        save_button.setStyleSheet("font-size: 20px; padding: 15px 25px; border-radius: 10px; background-color: green; color: white;")
        save_button.clicked.connect(self.save_data)

        bottom_layout.addWidget(save_button)
        self.canvas_layout.addLayout(bottom_layout)

    def create_assign_medicine_screen(self, patient_id):
        """Creates the Assign Medicine screen inside the canvas."""
        self.clear_layout(self.canvas_layout)

        # Header Layout
        header_layout = QHBoxLayout()

        title_label = QLabel("Assign Medicine")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px; padding: 10px;")
        header_layout.addWidget(title_label)

        patient_label = QLabel(f"Patient ID: {patient_id}")
        patient_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px; padding: 10px;")
        patient_label.setAlignment(Qt.AlignRight)
        header_layout.addWidget(patient_label)

        self.canvas_layout.addLayout(header_layout)

        # SubHeader
        label_layout = QHBoxLayout()
        for text in ["Morning", "Noon", "Evening"]:
            label = QLabel(text)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("font-size: 18px; font-weight: bold;")
            label_layout.addWidget(label)
        self.canvas_layout.addLayout(label_layout)

        # Medicine Table
        self.medicine_table = QTableWidget(1, 3)
        self.medicine_table.horizontalHeader().setVisible(False)
        self.medicine_table.verticalHeader().setVisible(False)
        self.medicine_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.medicine_table.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.medicine_table.setFont(QFont("Arial", 16))
        self.medicine_table.setRowHeight(0, 60)
        self.medicine_table.setStyleSheet("QTableWidget::item { padding: 20px; }")
        self.canvas_layout.addWidget(self.medicine_table)

       
        bottom_buttons_layout = QHBoxLayout()

        # Add Row Button
        add_row_button = QPushButton("+ Add Row")
        add_row_button.setStyleSheet("font-size: 18px; padding: 15px; border-radius: 10px; background-color: blue; color: white;")
        add_row_button.clicked.connect(self.add_medicine_row)
        bottom_buttons_layout.addWidget(add_row_button)

        bottom_buttons_layout.addStretch()

        # Cancel
        cancel_button = QPushButton("Cancel")
        cancel_button.setStyleSheet("font-size: 18px; padding: 15px; background-color: gray; color: white;")
        cancel_button.clicked.connect(self.create_inventory_table)
        bottom_buttons_layout.addWidget(cancel_button)

        # Confirm
        confirm_button = QPushButton("Confirm")
        confirm_button.setStyleSheet("font-size: 18px; padding: 15px; background-color: green; color: white;")
        confirm_button.clicked.connect(self.create_inventory_table)
        bottom_buttons_layout.addWidget(confirm_button)

        self.canvas_layout.addLayout(bottom_buttons_layout)

    def add_medicine_row(self):
        if self.medicine_table.rowCount() < 5:
            self.medicine_table.insertRow(self.medicine_table.rowCount())
            self.medicine_table.setRowHeight(self.medicine_table.rowCount() - 1, 60)
            
    def check_and_add_buttons(self, row, col):
        for i in range(4):
            item = self.table.item(row, i)
            if not item or item.text().strip() == "":
                return

        if not self.table.cellWidget(row, 4):
            attach_button = QPushButton("Attach Medicine")
            attach_button.setStyleSheet("font-size: 18px; padding: 15px; background-color: blue; color: white;")
            attach_button.clicked.connect(lambda: self.attach_medicine(row))
            self.table.setCellWidget(row, 4, attach_button)

    def attach_medicine(self, row):
        patient_id_item = self.table.item(row, 2)
        patient_id = patient_id_item.text() if patient_id_item else "Unknown"
        self.create_assign_medicine_screen(patient_id)

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            sub_layout = item.layout()

            if widget:
                widget.deleteLater()
            elif sub_layout:
                self.clear_layout(sub_layout)

    def save_data(self):
        print("Inventory Table data saved!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RobotDashboard()
    sys.exit(app.exec_())