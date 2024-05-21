import sys
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QObject
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
import cv2
import multiprocessing
from multiprocessing import Queue

class VideoThread(QThread):
    frame_signal = pyqtSignal(QImage)

    def run(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Convertir el frame de BGR a RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Crear una imagen QImage
            h, w, ch = rgb_frame.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)

            # Emitir la señal con el frame
            self.frame_signal.emit(qt_image)

        cap.release()

class FrameProcessorProcess(multiprocessing.Process):
    def __init__(self, input_queue, output_queue):
        super().__init__()
        self.input_queue = input_queue
        self.output_queue = output_queue

    def run(self):
        while True:
            frame = self.input_queue.get()
            # Realizar algún procesamiento en el frame (puedes personalizar esto según tus necesidades)

            # Colocar el frame procesado en la cola de salida
            self.output_queue.put(frame)

class FrameProcessor(QObject):
    frame_processed = pyqtSignal(QImage)

    def __init__(self, input_queue, output_queue):
        super().__init__()
        self.input_queue = input_queue
        self.output_queue = output_queue

    def start_processing(self):
        while True:
            if not self.input_queue.empty():
                frame = self.input_queue.get()
                # Realizar algún procesamiento en el frame (puedes personalizar esto según tus necesidades)

                # Emitir la señal con el frame procesado
                self.frame_processed.emit(frame)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.video_label = QLabel(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.video_label)

        self.input_queue = Queue()
        self.output_queue = Queue()

        self.video_thread = VideoThread(self)
        self.video_thread.frame_signal.connect(self.processed_frame_received)
        self.video_thread.start()

        self.frame_processor_process = FrameProcessorProcess(self.input_queue, self.output_queue)
        self.frame_processor_process.start()

        self.frame_processor = FrameProcessor(self.input_queue, self.output_queue)
        self.frame_processor.frame_processed.connect(self.update_video_label)
        self.frame_processor.start_processing()

    def processed_frame_received(self, qt_image):
        # Poner el frame en la cola de entrada para procesamiento
        frame_copy = qt_image.copy()  # Hacer una copia para evitar problemas de referencia
        self.input_queue.put(frame_copy)

    def update_video_label(self, qt_image):
        # Mostrar el frame procesado en un QLabel
        pixmap = QPixmap.fromImage(qt_image)
        self.video_label.setPixmap(pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setGeometry(100, 100, 800, 600)
    window.show()
    sys.exit(app.exec())
