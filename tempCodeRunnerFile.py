        hbox = QHBoxLayout()  # Horizontal box to center the grid
        hbox.setAlignment(Qt.AlignCenter)

        self.grid = QGridLayout()
        hbox.addLayout(self.grid)  # Place grid in the center
        layout.addLayout(hbox)