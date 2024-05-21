import sys
import cv2
from PyQt6.QtCore import QThread, pyqtSignal, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget
from PyQt6.QtGui import QImage, QPixmap
import multiprocessing
import time


class VideoThread(QThread):
    frame_signal = pyqtSignal(object)  # Señal para emitir frames

    def __init__(self, input_queue, output_queue, parent=None):
        super().__init__(parent)
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.is_running = False

    def run(self):
        self.is_running = True
        cap = cv2.VideoCapture(0)

        while self.is_running:
            ret, frame = cap.read()

            if not ret:
                break

            if not self.input_queue.full():
                self.input_queue.put(frame)

            time.sleep(0.02)  # Descanso para evitar el uso excesivo de la CPU

        cap.release()
        
class VideoProcess(multiprocessing.Process):
    def __init__(self, input_queue, output_queue):
        super().__init__()
        self.input_queue = input_queue
        self.output_queue = output_queue

    def run(self):
        while True:
            if not self.input_queue.empty():
                frame = self.input_queue.get()
                # Aquí puedes realizar el procesamiento de la imagen con OpenCV
                # Por ejemplo, podrías convertir la imagen a escala de grises
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Emitir el frame procesado a la cola de salida
                self.output_queue.put(gray_frame)
                time.sleep(0.02)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.processor_input_queue = multiprocessing.Queue(maxsize=10)
        self.processor_output_queue = multiprocessing.Queue(maxsize=10)

        self.processor_process = None
        self.video_thread = None

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Pyqt6 aplicacion")
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.label = QLabel(self)
        layout.addWidget(self.label)

        start_button = QPushButton("Iniciar", self)
        start_button.clicked.connect(self.start_video_thread)
        layout.addWidget(start_button)

        stop_button = QPushButton("Detener", self)
        stop_button.clicked.connect(self.stop_threads)
        layout.addWidget(stop_button)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        
        self.timer.start(50)  # Actualizar cada 50 milisegundos

    def start_video_thread(self):
        if self.video_thread is None or not self.video_thread.isRunning():
            # Inicializamos el hilo con las colas de entrada y salida del proceso
            self.processor_process = VideoProcess(self.processor_input_queue, self.processor_output_queue)
            self.video_thread = VideoThread(self.processor_input_queue, self.processor_output_queue)
            self.processor_process.start()
            self.video_thread.start()

    def update_frame(self):
        while not self.processor_output_queue.empty():
            processed_frame = self.processor_output_queue.get()

            qt_image = QImage(processed_frame.data, processed_frame.shape[1], processed_frame.shape[0],
                            processed_frame.strides[0], QImage.Format.Format_Grayscale8)
            pixmap = QPixmap.fromImage(qt_image)
            self.label.setPixmap(pixmap)

    def stop_threads(self):
        if self.video_thread is not None and self.video_thread.isRunning():
            self.video_thread.is_running = False
            self.video_thread.quit()
            self.video_thread.wait()

        if self.processor_process is not None and self.processor_process.is_alive():
            self.processor_process.terminate()
            self.processor_process.join()

    def closeEvent(self, event):
        try:
            # Terminate the process and close the PyQt6 application gracefully
            self.stop_threads()
            print("Final del código")
        except Exception as e:
            print(f"Excepción en stop_threads: {e}")

    




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())