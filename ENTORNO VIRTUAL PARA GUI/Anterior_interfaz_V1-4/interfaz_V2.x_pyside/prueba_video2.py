import sys
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget
import cv2
from queue import Queue
import numpy as np

class CaptureThread(QThread):
    captured_frame_signal = pyqtSignal(QImage)

    def __init__(self, camera_index, shared_frame_queue):
        super().__init__()
        self.camera_index = camera_index
        self.cap = cv2.VideoCapture(self.camera_index)
        self.shared_frame_queue = shared_frame_queue

        if not self.cap.isOpened():
            print(f"No se puede abrir la cámara {self.camera_index}")
            self.cap.release()
            self.terminate()

    def run(self):
        if not self.cap.isOpened():
            return

        while True:
            ret, frame = self.cap.read()
            if not ret:
                print(f"No se pudo capturar el marco de la cámara {self.camera_index}")
                break

            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            convert_to_qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            p = convert_to_qt_format.scaled(640, 480, Qt.AspectRatioMode.IgnoreAspectRatio)
            
            self.shared_frame_queue.put(p)  # Agregar el marco a la cola
            self.captured_frame_signal.emit(p)

        self.cap.release()

class ProcessThread(QThread):
    process_completed_signal = pyqtSignal(QImage)

    def __init__(self, thread_name, shared_frame_queue):
        super().__init__()
        self.thread_name = thread_name
        self.shared_frame_queue = shared_frame_queue

    def run(self):
        while True:
            if not self.shared_frame_queue.empty():
                frame = self.shared_frame_queue.get()
                # Realizar algún procesamiento en la imagen, por ejemplo, invertir colores
                processed_frame = self.invert_colors(frame)
                self.process_completed_signal.emit(processed_frame)

    def invert_colors(self, image):
        # Invertir los colores utilizando el método rgbSwapped() de PyQt
        inverted_image = image
        return inverted_image

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.image_label1 = QLabel(self)
        self.image_label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        

        self.image_label2 = QLabel(self)
        self.image_label2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.image_label3 = QLabel(self)
        self.image_label3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout(self.central_widget)
        layout.addWidget(self.image_label1)
        layout.addWidget(self.image_label2)
        layout.addWidget(self.image_label3)

        self.shared_frame_queue = Queue()  # Crear la cola compartida

        self.capture_thread = CaptureThread(0, self.shared_frame_queue)
        self.process_thread1 = ProcessThread("ProcessThread1", self.shared_frame_queue)
        self.process_thread2 = ProcessThread("ProcessThread2", self.shared_frame_queue)

        self.capture_thread.captured_frame_signal.connect(self.update_image1)
        self.process_thread1.process_completed_signal.connect(self.update_image2)
        self.process_thread2.process_completed_signal.connect(self.update_image3)

        self.capture_thread.start()
        self.process_thread1.start()
        self.process_thread2.start()

    def update_image1(self, image):
        self.image_label1.setPixmap(QPixmap.fromImage(image))

    def update_image2(self, image):
        self.image_label2.setPixmap(QPixmap.fromImage(image))

    def update_image3(self, image):
        self.image_label3.setPixmap(QPixmap.fromImage(image))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setGeometry(100, 100, 800, 600)
    window.show()
    sys.exit(app.exec())
