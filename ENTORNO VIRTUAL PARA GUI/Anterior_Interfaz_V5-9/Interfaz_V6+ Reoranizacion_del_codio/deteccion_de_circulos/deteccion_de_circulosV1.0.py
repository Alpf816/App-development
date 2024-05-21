from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QSlider, QWidget, QGridLayout
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt, QTimer
import cv2
import numpy as np

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.TonMin1 = 0
        self.PurMin1 = 60
        self.LumMin1 = 40
        self.TonMax1 = 255
        self.PurMax1 = 255
        self.LumMax1 = 255

        self.setup_ui()

        # Agregar la inicialización de la cámara aquí
        self.cap = cv2.VideoCapture(0)  # Puedes ajustar el índice según tu cámara

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Actualiza cada 30 milisegundos

    def setup_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QGridLayout()

        self.label_frame = QLabel(self)
        layout.addWidget(self.label_frame, 0, 0)

        self.label_mask = QLabel(self)
        layout.addWidget(self.label_mask, 0, 1)

        # Sliders for minimum HSV values
        self.slider_ton_min = self.create_slider("Ton Min", 0, 255, self.TonMin1, self.on_ton_min_change)
        self.slider_pur_min = self.create_slider("Saturation Min", 0, 255, self.PurMin1, self.on_pur_min_change)
        self.slider_lum_min = self.create_slider("lum Min", 0, 255, self.LumMin1, self.on_lum_min_change)

        # Sliders for maximum HSV values
        self.slider_ton_max = self.create_slider("Ton Max", 0, 255, self.TonMax1, self.on_ton_max_change)
        self.slider_pur_max = self.create_slider("Saturation Max", 0, 255, self.PurMax1, self.on_pur_max_change)
        self.slider_lum_max = self.create_slider("lum Max", 0, 255, self.LumMax1, self.on_lum_max_change)

        layout.addWidget(self.slider_ton_min, 1, 0)
        layout.addWidget(self.slider_pur_min, 2, 0)
        layout.addWidget(self.slider_lum_min, 3, 0)
        layout.addWidget(self.slider_ton_max, 1, 1)
        layout.addWidget(self.slider_pur_max, 2, 1)
        layout.addWidget(self.slider_lum_max, 3, 1)

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

        # Detección del centro del círculo y dibujo solo los círculos completamente llenos
        for contorno in contorno1:
            if 20 < len(contorno) < 250:
                # Calcular el área del contorno y del círculo encerrado por el límite convexo
                area_contorno = cv2.contourArea(contorno)
                hull = cv2.convexHull(contorno)
                area_hull = cv2.contourArea(hull)

                # Calcular el porcentaje de llenado
                porcentaje_llenado = (area_contorno / area_hull) * 100

                # Filtrar círculos con al menos el porcentaje requerido de llenado
                if porcentaje_llenado >= 90:
                    (x, y), radio = cv2.minEnclosingCircle(contorno)
                    centro = (int(x), int(y))
                    radio = int(radio)
                    cv2.circle(frame, centro, radio, (0, 255, 0), 2)
                     # Mostrar las coordenadas del centro en el frame
                    texto = f"Centro: ({centro[0]}, {centro[1]})"
                    cv2.putText(frame, texto, (centro[0] - 50, centro[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        if contour_image1 is not None and contour_image1.shape[0] > 0 and contour_image1.shape[1] > 0:
            qt_image_contour1 = QImage(frame.data, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format.Format_BGR888)
            pixmap_contour1 = QPixmap(qt_image_contour1)
            self.label_frame.setPixmap(pixmap_contour1)

            # Máscara de contorno1
            qt_image_mask = QImage(mascara1.data, mascara1.shape[1], mascara1.shape[0], mascara1.strides[0], QImage.Format.Format_Grayscale8)
            pixmap_mask = QPixmap(qt_image_mask)
            self.label_mask.setPixmap(pixmap_mask)

    def closeEvent(self, event):
        self.cap.release()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
