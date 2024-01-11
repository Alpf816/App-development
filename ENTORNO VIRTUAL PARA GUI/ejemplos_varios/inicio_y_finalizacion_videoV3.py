import sys
import cv2
from PyQt6.QtCore import QThread, pyqtSignal, QMutex, QMutexLocker
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget
import numpy as np

class CameraThread(QThread):
    frame_signal = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()
        self.camera = cv2.VideoCapture(0)
        self.running = True
        self.latest_frame = None
        self.frame_lock = QMutex()

    def get_latest_frame(self):
        with QMutexLocker(self.frame_lock):
            return self.latest_frame.copy() if self.latest_frame is not None else None

    def run(self):
        while self.running:
            ret, frame = self.camera.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                with QMutexLocker(self.frame_lock):
                    self.latest_frame = frame.copy()
                image = QImage(frame.data, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format.Format_RGB888)
                self.frame_signal.emit(image)

                # Agregar una pausa para evitar saturar el hilo principal
                QThread.msleep(50)

    def stop(self):
        self.running = False
        self.wait()
        self.camera.release()

class ImageProcessorThread(QThread):
    processed_frame_signal = pyqtSignal(QImage)

    def __init__(self, get_frame_function):
        super().__init__()
        self.running = True
        self.get_frame_function = get_frame_function

    def run(self):
        while self.running:
            frame = self.get_frame_function()
            if frame is not None:

                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Emitir la señal con la segunda imagen en formato escala de grises
                qt_gray_image = QImage(gray_frame.data, gray_frame.shape[1], gray_frame.shape[0], gray_frame.strides[0], QImage.Format.Format_Grayscale8)
                self.processed_frame_signal.emit(qt_gray_image)

                # Agregar una pausa para evitar saturar el hilo principal
                QThread.msleep(50)

    def stop(self):
        self.running = False
        self.wait()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Cámara con PyQt6 y OpenCV")

        # Crear widgets
        self.label = QLabel(self)
        self.label2 = QLabel(self)
        self.start_button = QPushButton("Encender cámara", self)
        self.stop_button = QPushButton("Apagar cámara", self)

        # Conectar botones a funciones
        self.start_button.clicked.connect(self.start_camera)
        self.stop_button.clicked.connect(self.stop_camera)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.label2)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Inicializar variables
        self.camera_thread = CameraThread()
        self.camera_thread.frame_signal.connect(self.update_frame)
        self.image_processor_thread = ImageProcessorThread(self.camera_thread.get_latest_frame)
        self.image_processor_thread.processed_frame_signal.connect(self.update_frame2)

        

    def start_camera(self):
        if not self.camera_thread.isRunning():
            self.camera_thread.start()
            self.image_processor_thread.start()

    def stop_camera(self):
        if self.camera_thread.isRunning():
            self.camera_thread.stop()
            self.image_processor_thread.stop()

    def update_frame(self, image):
        pixmap = QPixmap.fromImage(image)
        self.label.setPixmap(pixmap)
        

    def update_frame2(self, image2):
        pixmap2 = QPixmap.fromImage(image2)
        self.label2.setPixmap(pixmap2)

    def closeEvent(self, event):
        # Detener los hilos al cerrar la aplicación
        self.stop_camera()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    try:
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"Error: {e}")
