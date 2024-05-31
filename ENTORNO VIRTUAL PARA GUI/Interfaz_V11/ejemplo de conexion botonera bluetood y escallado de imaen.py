import cv2
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow, QSlider, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, pyqtSignal, QTimer

# Función para dibujar una línea de ayuda en el eje X
def draw_x_line(image, x_pos):
    cv2.line(image, (x_pos, 0), (x_pos, image.shape[0]), (0, 255, 0), 10)

# Función para dibujar una línea de ayuda en el eje Y
def draw_y_line(image, y_pos):
    cv2.line(image, (0, y_pos), (image.shape[1], y_pos), (0, 255, 0), 10)

# Función para cambiar la esquina de la imagen
def change_image_corner(image, x_pos, y_pos):
    # Definir las coordenadas de los puntos de la imagen original
    original_pts = np.float32([[0, 0], [image.shape[1], 0], [0, image.shape[0]], [image.shape[1], image.shape[0]]])
    
    # Definir las coordenadas de los puntos de destino (nueva esquina)
    destination_pts = np.float32([[image.shape[1]*x_pos[0], image.shape[0]*y_pos[0]],
                                   [image.shape[1]*x_pos[1], image.shape[0]*y_pos[1]],
                                   [image.shape[1]*x_pos[2], image.shape[0]*y_pos[2]],
                                   [image.shape[1]*x_pos[3], image.shape[0]*y_pos[3]]])
    
    # Calcular la matriz de transformación
    matrix = cv2.getPerspectiveTransform(original_pts, destination_pts)
    
    # Aplicar la transformación de perspectiva
    result = cv2.warpPerspective(image, matrix, (image.shape[1], image.shape[0]))
    
    return result

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Crear los sliders
        self.x_sliders = [QSlider(Qt.Orientation.Horizontal) for _ in range(4)]
        self.y_sliders = [QSlider(Qt.Orientation.Horizontal) for _ in range(4)]
        
        # Configurar los sliders
        for slider in self.x_sliders + self.y_sliders:
            slider.setMinimum(0)
            slider.setMaximum(100)
            slider.setValue(50)
            slider.setTickInterval(1)
            slider.setTickPosition(QSlider.TickPosition.TicksBelow)
            slider.valueChanged.connect(self.update_image)

        # Crear el layout vertical para los sliders
        layout = QVBoxLayout()
        for i in range(4):
            layout.addWidget(self.x_sliders[i])
            layout.addWidget(self.y_sliders[i])

        # Crear el widget central
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Leer la imagen
        self.image = cv2.imread('App-development/ENTORNO VIRTUAL PARA GUI/Interfaz_V11/placa de montaje.jpg', cv2.IMREAD_UNCHANGED)
        if self.image is not None:
            # Separar la imagen y el canal alfa
            bgra_planes = cv2.split(self.image)
            self.image = cv2.merge(bgra_planes[:3])

        # Timer para actualizar la imagen
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_image)
        self.timer.start(100)

    def update_image(self):
        x_pos = [slider.value() / 100 for slider in self.x_sliders]
        y_pos = [slider.value() / 100 for slider in self.y_sliders]
        if self.image is not None:
            updated_image = change_image_corner(self.image, x_pos, y_pos)
            cv2.imshow('Modified Image', updated_image)
            cv2.waitKey(1)

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
