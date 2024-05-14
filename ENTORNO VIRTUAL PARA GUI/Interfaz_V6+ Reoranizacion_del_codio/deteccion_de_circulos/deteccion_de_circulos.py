from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QSlider, QWidget,QGridLayout
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt, QTimer
import cv2
import numpy as np

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.TonMin1 = 0
        self.PurMin1 = 60
        self.LumMin1 = 0
        self.TonMax1 = 220
        self.PurMax1 = 255
        self.LumMax1 = 255
        self.cap = cv2.VideoCapture(0)  # Puedes ajustar el índice según tu cámara

        self.setup_ui()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Actualiza cada 30 milisegundos

    def setup_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QGridLayout()

        self.label = QLabel(self)
        layout.addWidget(self.label)

        # Sliders for minimum HSV values
        self.slider_ton_min = self.create_slider("Hue Min", 0, 255, self.TonMin1, self.on_ton_min_change)
        self.slider_pur_min = self.create_slider("Saturation Min", 0, 255, self.PurMin1, self.on_pur_min_change)
        self.slider_lum_min = self.create_slider("Value Min", 0, 255, self.LumMin1, self.on_lum_min_change)

        # Sliders for maximum HSV values
        self.slider_ton_max = self.create_slider("Hue Max", 0, 255, self.TonMax1, self.on_ton_max_change)
        self.slider_pur_max = self.create_slider("Saturation Max", 0, 255, self.PurMax1, self.on_pur_max_change)
        self.slider_lum_max = self.create_slider("Value Max", 0, 255, self.LumMax1, self.on_lum_max_change)

        layout.addWidget(self.slider_ton_min)
        layout.addWidget(self.slider_pur_min)
        layout.addWidget(self.slider_lum_min)
        layout.addWidget(self.slider_ton_max)
        layout.addWidget(self.slider_pur_max)
        layout.addWidget(self.slider_lum_max)

        central_widget.setLayout(layout)

    def create_slider(self, label, min_val, max_val, default_val, slot):
        slider = QSlider()
        slider.setOrientation(Qt.Orientation.Horizontal)
        slider.setMinimum(min_val)
        slider.setMaximum(max_val)
        slider.setValue(default_val)
        slider.valueChanged.connect(slot)

        label_widget = QLabel(label)
        layout = QVBoxLayout()
        layout.addWidget(label_widget)
        layout.addWidget(slider)

        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def on_ton_min_change(self, value):
        self.TonMin1 = value

    def on_pur_min_change(self, value):
        self.PurMin1 = value

    def on_lum_min_change(self, value):
        self.LumMin1 = value

    def on_ton_max_change(self, value):
        self.TonMax1 = value

    def on_pur_max_change(self, value):
        self.PurMax1 = value

    def on_lum_max_change(self, value):
        self.LumMax1 = value

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        hsv1 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        color_oscuro1 = np.array([self.TonMin1, self.PurMin1, self.LumMin1])
        color_claro1 = np.array([self.TonMax1, self.PurMax1, self.LumMax1])
        mascara1 = cv2.inRange(hsv1, color_oscuro1, color_claro1)

        contorno1, _ = cv2.findContours(mascara1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contour_image1 = np.zeros((frame.shape[0], frame.shape[1], 3), dtype=np.uint8)

        # Definir un umbral de área mínimo (ajústalo según tus necesidades)
        area_minima = 400

        # Detección del centro del círculo y dibujo solo los círculos dentro de contorno1
        for contorno in contorno1:
            if len(contorno) > 5:
                # Calcular el área del contorno
                area_contorno = cv2.contourArea(contorno)
                
                # Filtrar contornos con áreas mayores al umbral
                if area_contorno > area_minima:
                    (x, y), radio = cv2.minEnclosingCircle(contorno)
                    centro = (int(x), int(y))
                    radio = int(radio)
                    cv2.circle(frame, centro, radio, (0, 255, 0), 2)

        if contour_image1 is not None and contour_image1.shape[0] > 0 and contour_image1.shape[1] > 0:
            qt_image_contour1 = QImage(frame.data, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format.Format_BGR888)
            pixmap = QPixmap(qt_image_contour1)
            self.label.setPixmap(pixmap)

        # Asegúrate de liberar recursos y cerrar la cámara al cerrar la aplicación
    def closeEvent(self, event):
        self.cap.release()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
