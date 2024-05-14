import cv2
import sys
import numpy as np
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QSlider, QWidget
from multiprocessing import Process, Queue, Value

class ImageProcessor(Process):
    def __init__(self, input_queue, output_queue, slider_value):
        super().__init__()
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.slider_value = slider_value

    def run(self):
        while True:
            frame = self.input_queue.get()  # Espera a recibir un frame desde el hilo principal

            # Ajusta el brillo de la imagen según el valor del slider
            adjusted_frame = cv2.convertScaleAbs(frame, alpha=1 + self.slider_value.value / 100.0, beta=0)
            print(self.slider_value.value)

            # Coloca el frame procesado en la cola de salida
            self.output_queue.put(adjusted_frame)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Configura las colas para la comunicación entre los procesos
        self.input_queue = Queue()
        self.output_queue = Queue()

        # Valor inicial del slider
        self.slider_value = Value('i', 0)

        self.setup_ui()

        # Inicia el proceso de procesamiento de imágenes
        self.image_processor = ImageProcessor(self.input_queue, self.output_queue, self.slider_value)
        self.image_processor.start()

    def setup_ui(self):
        self.label = QLabel(self)
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(0)
        self.slider.setSingleStep(10)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.slider)

        self.setLayout(layout)

        self.setWindowTitle("OpenCV y PyQt6")

        # Conecta la señal del slider directamente al método de actualización
        self.slider.valueChanged.connect(self.update_slider_value)

        # Configura un temporizador para actualizar la GUI
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_gui)
        self.timer.start(50)

        # Inicia el hilo de captura de frames
        self.image_thread = ImageThread(self.input_queue)
        self.image_thread.frame_captured.connect(self.process_frame)
        self.image_thread.start()

    @pyqtSlot(np.ndarray)
    def process_frame(self, frame):
        # Pasa el frame al proceso de procesamiento
        self.input_queue.put(frame)

    def update_slider_value(self, value):
        # Actualiza el valor del slider y envía el nuevo valor al proceso de procesamiento
        self.slider_value.value = value

    def update_gui(self):
        # Revisa la cola de salida para obtener el frame procesado y mostrarlo en el QLabel
        while not self.output_queue.empty():
            processed_frame = self.output_queue.get()
            self.update_image(processed_frame)

    @pyqtSlot(np.ndarray)
    def update_image(self, image):
        # Convierte la imagen de OpenCV a QImage y muestra en el QLabel
        height, width, channel = image.shape
        bytes_per_line = 3 * width
        q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        self.label.setPixmap(pixmap)

    def closeEvent(self, event):
        # Detiene el proceso de procesamiento de imágenes antes de cerrar la aplicación
        self.image_processor.terminate()
        self.image_thread.terminate()
        
        # Libera la cámara
        cv2.VideoCapture(0).release()
        
        event.accept()

class ImageThread(QThread):
    frame_captured = pyqtSignal(np.ndarray)

    def __init__(self, input_queue):
        super().__init__()
        self.input_queue = input_queue

    def run(self):
        cap = cv2.VideoCapture(0)  # Puedes ajustar el número de la cámara según tus necesidades

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Emitir la señal con el frame capturado
            self.frame_captured.emit(frame)

        cap.release()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
