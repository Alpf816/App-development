import sys
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtGui import QImage, QPixmap, QPainter
from PyQt6.QtCore import Qt
import cv2
from PIL import Image, ImageDraw, ImageQt

def crear_plano_cartesiano(ancho, alto):
    imagen = Image.new("RGB", (ancho, alto), "white")
    dibujo = ImageDraw.Draw(imagen)

    dibujo.line([(0, alto - 1), (ancho - 1, alto - 1)], fill="black")
    dibujo.line([(0, alto - 1), (0, 0)], fill="black")

    for i in range(0, ancho, 20):
        dibujo.line([(i, alto - 1), (i, alto - 5)], fill="black")
    for i in range(0, alto, 20):
        dibujo.line([(0, alto - i - 1), (5, alto - i - 1)], fill="black")

    return imagen

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.inicializar_ui()

        self.cap = cv2.VideoCapture(0)
        self.actualizar_video()

    def inicializar_ui(self):
        self.setWindowTitle('Video con Plano Cartesiano')

        self.etiqueta_video = QLabel(self)
        self.etiqueta_video.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.etiqueta_video)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.ancho = 640
        self.alto = 480

        self.plano_cartesiano = crear_plano_cartesiano(self.ancho, self.alto)

    def actualizar_video(self):
        ret, frame = self.cap.read()

        if ret:
            imagen_qt = ImageQt.ImageQt(self.plano_cartesiano)
            pixmap_cartesiano = QPixmap.fromImage(imagen_qt)

            imagen = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            altura, ancho, _ = imagen.shape
            imagen_qt = QImage(imagen.data, ancho, altura, ancho * 3, QImage.Format.Format_RGB888)
            pixmap_video = QPixmap.fromImage(imagen_qt)

            pixmap_resultante = pixmap_video.copy()
            painter = QPainter(pixmap_resultante)
            painter.drawPixmap(0, 0, pixmap_cartesiano)
            painter.end()

            self.etiqueta_video.setPixmap(pixmap_resultante)

        self.actualizar_video()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())
