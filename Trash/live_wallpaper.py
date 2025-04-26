import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import scipy.ndimage
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class LiveWallpaperWidget(FigureCanvas):
    def __init__(self, parent=None):
        self.widget_width, self.widget_height = parent.width(), parent.height()
        
        fig, ax = plt.subplots(figsize=(self.widget_width / 100, self.widget_height / 100))
        
        # 🔹 Call the superclass constructor first
        super().__init__(fig)
        self.setParent(parent)

        self.ax = ax
        self.setFixedSize(self.widget_width, self.widget_height)  # Ensure correct widget size
        self.ax.axis('off')

        fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
        fig.tight_layout(pad=0)

        # Apply the gradient background
        self.gradient_background()

        # Initialize wave animation
        self.num_waves = 7
        self.colors = ["#ff6666", "#ff4d4d", "#ff3333", "#ff1a1a", "#e60000", "#cc0000", "#990000"]
        self.base_frequencies = np.linspace(0.004, 0.012, self.num_waves)
        self.base_amplitudes = np.linspace(50, 300, self.num_waves)
        self.phases = np.linspace(0, np.pi, self.num_waves)
        self.lines = [self.ax.plot([], [], color=self.colors[i], linewidth=3, alpha=0.8)[0] for i in range(self.num_waves)]

        # Timer for animation
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # 30ms update rate
        self.frame = 0


    def gradient_background(self):
        color1, color2 = "#220000", "#550000"
        gradient = np.linspace(0, 1, 256)
        gradient = np.vstack((gradient, gradient))
        self.ax.imshow(gradient, aspect="auto", extent=[0, self.widget_width, 0, self.widget_height],
                       cmap=mcolors.LinearSegmentedColormap.from_list("grad", [color1, color2]), origin='lower')

    def update_frame(self):
        x = np.linspace(0, self.widget_width, 1000)
        for i, line in enumerate(self.lines):
            freq_variation = np.sin(self.frame * 0.01 + self.phases[i]) * 0.005  
            amplitude_variation = np.cos(self.frame * 0.02 + self.phases[i]) * 30  
            depth_modulation = np.sin(x * 0.001 + self.frame * 0.05) * 20  

            freq = self.base_frequencies[i] + freq_variation
            amplitude = self.base_amplitudes[i] + amplitude_variation

            y = amplitude * np.sin(freq * x + self.phases[i] + self.frame * 0.1) + self.widget_height // 2 + depth_modulation
            if i % 2 == 0:  
                y = scipy.ndimage.gaussian_filter1d(y, sigma=10)

            line.set_data(x, y)

        self.frame += 1
        self.draw()
