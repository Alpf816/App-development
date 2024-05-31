import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QSlider, QVBoxLayout, QWidget, QPushButton, QLineEdit, QHBoxLayout, QComboBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap, QGuiApplication, QIntValidator
import cv2
import numpy as np

class ImageWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Imagen Sin Bordes')
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self.label = QLabel(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        self.setLayout(layout)

    def update_image(self, image):
        height, width, channel = image.shape
        bytes_per_line = 3 * width
        q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(q_image))

    def adjust_window_position(self):
        # Obtener la lista de pantallas disponibles
        screen_list = QGuiApplication.screens()

        # Verificar si hay al menos dos pantallas disponibles
        if len(screen_list) > 1:
            # Obtener la geometría de la segunda pantalla
            second_screen_geometry = screen_list[1].geometry()

            # Calcular la nueva posición de la ventana
            new_x = int(second_screen_geometry.x() - 11)
            new_y = int(second_screen_geometry.y() - 11)

            # Establecer la nueva posición de la ventana
            self.move(new_x, new_y)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Controles')

        self.sub_image_path = 'App-development/ENTORNO VIRTUAL PARA GUI/Interfaz_V12/Aruco_8.jpg'
        self.center = (600, 400)  # Centro de la imagen principal
        self.distance = 50

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(1200)
        self.slider.setValue(self.distance)
        self.slider.valueChanged.connect(self.slider_changed)

        self.button = QPushButton("Procesar Imagen")
        self.button.clicked.connect(self.start_processing)

        self.x_input = QLineEdit()
        self.x_input.setValidator(QIntValidator())
        self.x_input.setText(str(self.center[0]))
        self.x_input.setPlaceholderText("Posición X")
        self.x_input.textChanged.connect(self.update_center_x)

        self.y_input = QLineEdit()
        self.y_input.setValidator(QIntValidator())
        self.y_input.setText(str(self.center[1]))
        self.y_input.setPlaceholderText("Posición Y")
        self.y_input.textChanged.connect(self.update_center_y)

        self.aspect_ratio_box = QComboBox()
        self.aspect_ratio_box.addItems(["1:1", "16:9","Automatico"])
        self.aspect_ratio_box.currentIndexChanged.connect(self.update_aspect_ratio)

        layout = QVBoxLayout()
        layout.addWidget(self.slider)
        layout.addWidget(self.button)

        position_layout = QHBoxLayout()
        position_layout.addWidget(self.x_input)
        position_layout.addWidget(self.y_input)

        layout.addLayout(position_layout)
        layout.addWidget(self.aspect_ratio_box)


        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.image_window = ImageWindow()
        self.image_window.show()
        self.image_window.adjust_window_position()

        self.aspect_ratio = "1:1"

    def slider_changed(self, value):
        self.distance = value

    def update_center_x(self, text):
        if text:
            self.center = (int(text), self.center[1])

    def update_center_y(self, text):
        if text:
            self.center = (self.center[0], int(text))

    def update_aspect_ratio(self):
        self.aspect_ratio = self.aspect_ratio_box.currentText()

    def start_processing(self):
        # Realizar el procesamiento de la imagen directamente en el método
        image = self.process_image(self.sub_image_path, self.center, self.distance, self.aspect_ratio)
        self.image_window.update_image(image)

    def process_image(self, sub_image_path, center, distance, aspect_ratio):
        # Crear una imagen en blanco
        image_width = 1905
        image_height = 1065
        main_image = np.ones((image_height, image_width, 3), dtype=np.uint8) * 255
        sub_image = cv2.imread(sub_image_path)

        sub_height, sub_width, _ = sub_image.shape

        if aspect_ratio == "16:9":
            distance_y = int(distance * 9 / 16)

        else:
            distance_y = distance

        positions = [
            (center[0] - sub_width // 2, center[1] - distance_y - sub_height // 2),  # Arriba
            (center[0] - sub_width // 2, center[1] + distance_y - sub_height // 2),  # Abajo
            (center[0] - distance - sub_width // 2, center[1] - sub_height // 2),  # Izquierda
            (center[0] + distance - sub_width // 2, center[1] - sub_height // 2)   # Derecha
        ]

        for pos in positions:
            x, y = pos
            if 0 <= x < main_image.shape[1] - sub_width and 0 <= y < main_image.shape[0] - sub_height:
                main_image[y:y + sub_height, x:x + sub_width] = sub_image

        return main_image

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
