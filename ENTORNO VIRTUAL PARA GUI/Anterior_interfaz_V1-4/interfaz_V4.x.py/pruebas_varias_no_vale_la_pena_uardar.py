import sys
import cv2
import numpy as np
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt, QTimer

class ImageOverlayApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.video_capture = cv2.VideoCapture(0)  # Abre la cámara (puedes cambiar 0 por el índice de tu cámara)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.video_label = QLabel(self)
        self.layout.addWidget(self.video_label)

        # Crea el plano cartesiano y la imagen de salida durante la inicialización
        self.coordinate_image = self.create_cartesian_plane_custom(width=640, height=480, scale=50,Inicio_px_X=50,Inicio_px_Y=100)
        self.overlay_frame = np.zeros_like(self.coordinate_image)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Actualiza cada 30 milisegundos

    def create_cartesian_plane_custom(self, width, height, scale,Inicio_px_X,Inicio_px_Y):
        image = np.zeros((height, width, 3), dtype=np.uint8)

        # Dibuja los ejes X e Y
        cv2.line(image, (0, height - 1), (width - 1, height - 1), (255, 255, 255), 2)
        cv2.line(image, (0, 0), (0, height - 1), (255, 255, 255), 2)

        # Dibuja las marcas cada `scale` píxeles en los ejes y las etiquetas con las coordenadas
        for x in range(0, width, scale):
            cv2.line(image, (x, height - 6), (x, height - 1), (255, 255, 255), 2)
            cv2.putText(image, str(x+Inicio_px_X), (x, height - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        for y in range(0, height, scale):
            cv2.line(image, (0, height - y), (5, height - y), (255, 255, 255), 2)
            cv2.putText(image, str(y+Inicio_px_Y), (8, height - y + 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        return image

    def update_frame(self):
        ret, frame = self.video_capture.read()

        if ret:
            # Actualiza solo el contenido necesario en lugar de recrear la imagen de salida
            self.overlay_frame[:, :] = self.overlay_images(frame, self.coordinate_image)

            # Convierte la imagen para mostrar en QLabel
            height, width, channel = self.overlay_frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(self.overlay_frame.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)

            # Muestra la imagen en el QLabel
            self.video_label.setPixmap(pixmap)

    def overlay_images(self, background, overlay):
        # Asegúrate de que las imágenes tengan el mismo tamaño
        overlay = cv2.resize(overlay, (background.shape[1], background.shape[0]))

        # Combina las imágenes
        result = cv2.addWeighted(background, 1, overlay, 0.5, 0)

        return result

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageOverlayApp()
    window.show()
    sys.exit(app.exec())