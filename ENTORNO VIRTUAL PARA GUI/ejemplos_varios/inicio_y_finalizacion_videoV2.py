import sys
import cv2
from PyQt6.QtCore import QThread, pyqtSignal
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

    def run(self):
        while self.running:
            ret, frame = self.camera.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.latest_frame = frame.copy()
                image = QImage(frame.data, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format.Format_RGB888)
                self.frame_signal.emit(image)
                

    def stop(self):
        self.running = False
        self.wait()
        self.camera.release()

class ImageProcessorThread(QThread):
    processed_frame_signal = pyqtSignal(QImage)
    

    def __init__(self, camera_thread):
        super().__init__()
        self.running = True
        self.camera_thread = camera_thread
        print("inicio ImageProcessorThread")
    

    def run(self):
        while self.running:
            self.msleep(10)
            
            frame = self.camera_thread.latest_frame
            if frame is not None:

                processed_frame = np.copy(frame)
                processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_RGB2GRAY)

                # Aplicar un filtro de escala de grises (ya estás en escala de grises)
                # Puedes realizar cualquier procesamiento adicional aquí

                # Convertir la imagen procesada a formato QImage
                height, width = processed_frame.shape
                bytes_per_line = 1 * width
                qt_image = QImage(processed_frame.data, width, height, bytes_per_line, QImage.Format.Format_Grayscale8)

                # Emitir la señal con la imagen procesada al hilo principal
                self.processed_frame_signal.emit(qt_image)
                self.msleep(10)
                
                print("final ImageProcessorThread")
                ######################################################################

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
        print("label1 añadido")
        layout.addWidget(self.label2)
        print("label2 añadido")
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Inicializar variables
        self.camera_thread = CameraThread()
        self.camera_thread.frame_signal.connect(self.update_frame)
        self.image_processor_thread = ImageProcessorThread(self.camera_thread)
        self.image_processor_thread.processed_frame_signal.connect(self.update_frame2)

    def start_camera(self):
        if not self.camera_thread.isRunning():
            self.camera_thread.start()
            self.image_processor_thread.start()
            print("boton de iniciar camara presionado.")

    def stop_camera(self):
        if self.camera_thread.isRunning():
            self.camera_thread.stop()
            self.image_processor_thread.stop()
            print("boton de apagar camara presionado.")
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
        print("Mi programa ha terminado de ejecutarse.")
    except Exception as e:
        print(f"Error: {e}")
