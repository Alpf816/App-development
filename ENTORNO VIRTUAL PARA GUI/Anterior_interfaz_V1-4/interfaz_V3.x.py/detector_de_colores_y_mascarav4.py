from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QSlider, QVBoxLayout, QWidget

import cv2
import numpy as np

class ColorTrackingApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Color Tracking App")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.video_label = QLabel(self)
        self.param_layout = QVBoxLayout()

        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_layout.addWidget(self.video_label)
        self.central_layout.addLayout(self.param_layout)

        self.tonalidad_minima = 0
        self.tonalidad_maxima = 255
        self.pureza_minima = 0
        self.pureza_maxima = 255
        self.luminosidad_minima = 0
        self.luminosidad_maxima = 255
        self.kernel_x = 1
        self.kernel_y = 1

        self.create_sliders()

        self.cap = cv2.VideoCapture(0)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_video)
        self.timer.start(30)  # Actualiza cada 30 ms (puedes ajustar esto según sea necesario)

    def create_sliders(self):
        parameters = [
            ("Tonalidad minima", 0, 255),
            ("Tonalidad maxima", 255, 255),
            ("pureza minima", 0, 255),
            ("pureza maxima", 255, 255),
            ("luminosidad minima", 0, 255),
            ("luminosidad maxima", 255, 255),
            ("Kernel X", 1, 30),
            ("Kernel Y", 1, 30),
        ]

        for name, default, max_value in parameters:
            slider = QSlider(Qt.Orientation.Horizontal)
            slider.setMinimum(0)
            slider.setMaximum(max_value)
            slider.setValue(default)
            slider.setTickPosition(QSlider.TickPosition.TicksBelow)
            slider.setTickInterval(1)
            slider.valueChanged.connect(lambda value, name=name: self.update_params(name, value))

            self.param_layout.addWidget(QLabel(name))
            self.param_layout.addWidget(slider)

    def update_params(self, name, value):
        setattr(self, name.replace(" ", "_").lower(), value)

    def update_video(self):
        ret, frame = self.cap.read()

        if ret:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            color_oscuro = np.array([self.tonalidad_minima, self.pureza_minima, self.luminosidad_minima])
            color_claro = np.array([self.tonalidad_maxima, self.pureza_maxima, self.luminosidad_maxima])

            mascara = cv2.inRange(hsv, color_oscuro, color_claro)

            kernel = np.ones((self.kernel_x, self.kernel_y), np.uint8)

            mascara = cv2.morphologyEx(mascara, cv2.MORPH_CLOSE, kernel)
            mascara = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, kernel)

            contorno, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(frame, contorno, -1, (0, 0, 0), 2)

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = image.shape
            bytes_per_line = ch * w
            qt_image = QImage(image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)

            self.video_label.setPixmap(pixmap)
            self.central_widget.repaint()

    def closeEvent(self, event):
        self.cap.release()
        self.timer.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication([])
    window = ColorTrackingApp()
    window.show()
    app.exec()
