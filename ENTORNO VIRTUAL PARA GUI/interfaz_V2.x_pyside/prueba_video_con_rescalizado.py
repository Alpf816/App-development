import sys
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, QTimer
import cv2
from PyQt6.QtGui import QImage, QPixmap

class VideoStreamWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.video_capture = cv2.VideoCapture(0)  # 0 para la cámara predeterminada

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout(self)
        layout.addWidget(self.image_label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Actualizar cada 30 milisegundos

    def update_frame(self):
        ret, frame = self.video_capture.read()
        if ret:
            # Escalar la imagen para que se ajuste al tamaño del QLabel
            frame = cv2.resize(frame, (self.width(), self.height()))
            height, width, channel = frame.shape

            q_image = QImage(frame.data, width, height, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.image_label.setPixmap(pixmap)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = VideoStreamWidget(self)
        self.setCentralWidget(self.central_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
