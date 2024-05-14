import sys
import cv2
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QImage, QPixmap
import numpy as np

class WebcamApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.video_capture = cv2.VideoCapture(0)  # 0 para la cámara predeterminada
        self.width_video_capture = int(self.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height_video_capture = int(self.video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print(f"Resolución de la cámara: {self.width_video_capture}x{self.height_video_capture}")
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.video_label = QLabel(self)
        self.layout.addWidget(self.video_label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Actualiza cada 30 milisegundos

    def create_cartesian_plane_custom(self, roi_width, roi_height, scale, Inicio_px_X, Inicio_px_Y):
        # Calcula las dimensiones del plano cartesiano según las dimensiones de la ROI
        width = roi_width
        height = roi_height
        image = np.zeros((height, width, 3), dtype=np.uint8)

        # Dibuja los ejes X e Y
        cv2.line(image, (0, height - 1), (width - 1, height - 1), (255, 255, 255), 2)
        cv2.line(image, (0, 0), (0, height - 1), (255, 255, 255), 2)

        # Dibuja las marcas cada `scale` píxeles en los ejes y las etiquetas con las coordenadas
        for x in range(0, width, scale):
            cv2.line(image, (x, height - 6), (x, height - 1), (255, 255, 255), 2)
            cv2.putText(image, str(x + Inicio_px_X), (x, height - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        for y in range(0, height, scale):
            cv2.line(image, (0, height - y), (5, height - y), (255, 255, 255), 2)
            cv2.putText(image, str(y + Inicio_px_Y), (8, height - y + 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        return image

    def update_frame(self):
        ret, frame = self.video_capture.read()
        if ret:
            # Aquí defines las coordenadas de la ROI
            roi_x, roi_y, roi_width, roi_height = 0, 0, 400, 400

            # Recortas la ROI del frame
            roi = frame[roi_y:roi_y + roi_height, roi_x:roi_x + roi_width]

            # Conviertes la ROI a escala de grises
            roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

            # Dibujas un marco alrededor de la ROI
            cv2.rectangle(frame, (roi_x, roi_y), (roi_x + roi_width, roi_y + roi_height), (0, 255, 0), 2)

            # Crea el plano cartesiano con las dimensiones de la ROI
            coordinate_image = self.create_cartesian_plane_custom(roi_width, roi_height, scale=100, Inicio_px_X=roi_x, Inicio_px_Y=roi_y)

            # Combina la ROI en escala de grises con el plano cartesiano
            combined_image = self.overlay_images(roi_gray, coordinate_image)

            # Conviertes la imagen combinada en escala de grises a un formato adecuado para mostrar en QLabel
            height, width = combined_image.shape
            bytes_per_line = width
            q_image = QImage(combined_image.data, width, height, bytes_per_line, QImage.Format.Format_Grayscale8)
            pixmap = QPixmap.fromImage(q_image)

            # Muestras la imagen en la QLabel
            self.video_label.setPixmap(pixmap)

    def overlay_images(self, background, overlay):
        # Asegúrate de que las imágenes tengan el mismo tamaño
        overlay = cv2.resize(overlay, (background.shape[1], background.shape[0]))

        # Si las imágenes tienen diferentes canales, convierte a escala de grises
        if overlay.shape[-1] != background.shape[-1]:
            overlay = cv2.cvtColor(overlay, cv2.COLOR_BGR2GRAY)

        # Combina las imágenes
        result = cv2.addWeighted(background, 1, overlay, 0.5, 0)

        return result
    def closeEvent(self, event):
        if self.video_capture is not None:
            self.video_capture.release()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WebcamApp()
    window.show()
    sys.exit(app.exec())
