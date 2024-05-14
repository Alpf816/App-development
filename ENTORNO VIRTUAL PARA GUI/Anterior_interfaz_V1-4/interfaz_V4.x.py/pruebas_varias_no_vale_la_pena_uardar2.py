import sys
import cv2
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QImage, QPixmap

class WebcamApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.video_capture = cv2.VideoCapture(0)  # 0 para la cámara predeterminada

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.video_label = QLabel(self)
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout(self.central_widget)
        layout.addWidget(self.video_label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Actualiza cada 30 milisegundos

    def update_frame(self):
        ret, frame = self.video_capture.read()

        # Aquí defines las coordenadas de la ROI
        roi_x, roi_y, roi_width, roi_height = 100, 100, 200, 200

        # Recortas la ROI del frame
        roi = frame[roi_y:roi_y + roi_height, roi_x:roi_x + roi_width]

        # Conviertes la ROI a escala de grises
        roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        # Dibujas un marco alrededor de la ROI
        cv2.rectangle(frame, (roi_x, roi_y), (roi_x + roi_width, roi_y + roi_height), (0, 255, 0), 2)

        # Conviertes la imagen de la ROI en escala de grises a un formato adecuado para mostrar en QLabel
        height, width = roi_gray.shape
        bytes_per_line = width
        q_image = QImage(roi_gray.data, width, height, bytes_per_line, QImage.Format.Format_Grayscale8)
        pixmap = QPixmap.fromImage(q_image)

        # Muestras la imagen en la QLabel
        self.video_label.setPixmap(pixmap)

    def closeEvent(self, event):
        self.video_capture.release()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WebcamApp()
    window.show()
    sys.exit(app.exec())
