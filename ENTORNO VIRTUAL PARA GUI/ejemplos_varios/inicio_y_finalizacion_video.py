import cv2
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
import numpy as np

class VideoThread(QThread):
    new_frame_signal = pyqtSignal(np.ndarray)

    def __init__(self, video_source):
        super(VideoThread, self).__init__()
        self.video_source = video_source
        self.cap = cv2.VideoCapture(video_source)

    def run(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                self.new_frame_signal.emit(frame)
            else:
                break

    def stop(self):
        self.cap.release()

class ImageProcessingThread(QThread):
    new_processed_frame_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super(ImageProcessingThread, self).__init__()
        self.frame = None  # Inicializar la variable frame

    def run(self):
        while True:
            if self.frame is not None:
                # Aquí puedes realizar tus operaciones de procesamiento en el frame
                processed_frame = self.frame.copy()  # Hacer una copia del frame
                # Realizar modificaciones en el processed_frame según sea necesario
                
                
                self.new_processed_frame_signal.emit(processed_frame)

    def set_frame(self, frame):
        self.frame = frame

class VideoWidget(QWidget):
    def __init__(self, parent=None):
        super(VideoWidget, self).__init__(parent)

        self.video_label1 = QLabel(self)
        self.video_label2 = QLabel(self)
        self.video_thread = VideoThread(0)  # Puedes ajustar el número según tu configuración
        self.image_processing_thread = ImageProcessingThread()

        layout = QVBoxLayout(self)
        layout.addWidget(self.video_label1)
        layout.addWidget(self.video_label2)

        self.video_thread.new_frame_signal.connect(self.update_video_frame)
        self.image_processing_thread.new_processed_frame_signal.connect(self.update_processed_frame)

        self.video_thread.start()
        self.image_processing_thread.start()

    def update_video_frame(self, frame):
        # Actualizar el QLabel con el frame del video
        img = QImage(frame.data, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format.Format_BGR888)
        pixmap = QPixmap.fromImage(img)
        self.video_label1.setPixmap(pixmap)

        # Enviar el frame al hilo de procesamiento de imágenes
        self.image_processing_thread.set_frame(frame)

    def update_processed_frame(self, processed_frame):
        # Puedes realizar acciones específicas aquí con el frame procesado
        pass
 

if __name__ == "__main__":
    app = QApplication([])
    window = VideoWidget()
    window.show()
    app.exec()
