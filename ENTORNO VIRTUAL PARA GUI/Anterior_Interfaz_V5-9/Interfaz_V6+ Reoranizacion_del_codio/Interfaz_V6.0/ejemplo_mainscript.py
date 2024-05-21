import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QThread, pyqtSignal, QTimer
from process_ejemplo import VideoProcess
import cv2
import multiprocessing
import time

def main():
    print("Inicio Mainscript")
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

class VideoThread(QThread):
    def __init__(self, input_queue):
        super().__init__()
        self.input_queue = input_queue
        self.is_running = False
        print("init tread")

    def run(self):
        print("inicio tread")
        self.is_running = True
        cap = cv2.VideoCapture(0)

        while self.is_running:
            ret, frame = cap.read()

            if not ret:
                break

            if not self.input_queue.full():
                self.input_queue.put(frame)

            QThread.msleep(50)

        cap.release()
        print("Finalizacion videotread")

class treadbucle(QThread):
    def __init__(self, señal_queue):
        super().__init__()
        self.a = 1
        self.señal_queue = señal_queue

    def run(self):
        print("Inicio treadbucle")
        while True:
            if not self.señal_queue.empty():
                señal = self.señal_queue.get()
                if not señal:
                    break

            print(str(self.a))
            self.a = self.a + 1
            QThread.msleep(1000)
        print("Finalizar treadbucle")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.processor_input_queue = multiprocessing.Queue(maxsize=10)
        self.processor_output_queue = multiprocessing.Queue(maxsize=10)
        self.señal_queue =  multiprocessing.Queue(maxsize=10)
        self.señal = True
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
        self.señal = True
        self.señal_queue.put(self.señal)
        if self.video_thread is None or not self.video_thread.isRunning():
            print("Iniciando video_thread y processor_process")
            self.processor_process = VideoProcess(self.processor_input_queue, self.processor_output_queue)
            self.video_thread = VideoThread(self.processor_input_queue)
            self.treadbucle = treadbucle(self.señal_queue)
            self.processor_process.start()
            self.video_thread.start()
            self.treadbucle.start()

    def update_frame(self):
        while not self.processor_output_queue.empty():
            processed_frame = self.processor_output_queue.get()

            qt_image = QImage(processed_frame.data, processed_frame.shape[1], processed_frame.shape[0],
                            processed_frame.strides[0], QImage.Format.Format_Grayscale8)
            pixmap = QPixmap.fromImage(qt_image)
            self.label.setPixmap(pixmap)

    def stop_threads(self):

        self.señal = False
        self.señal_queue.put(self.señal)
        

        if self.video_thread is not None and self.video_thread.isRunning():
            
            self.video_thread.is_running = False
            self.video_thread.quit()
            self.video_thread.wait()

        if self.processor_process is not None and self.processor_process.is_alive():
            
            self.processor_process.terminate()
            self.processor_process.join()
            print("processo finalizado")
            
        if self.treadbucle is not None and self.treadbucle.isRunning():
            self.treadbucle.quit()
            self.treadbucle.wait()

        

            print("treadbucle finalizado")

    def closeEvent(self, event):
        try:
            # Terminate the process and close the PyQt6 application gracefully
            print("Final del código")
            self.stop_threads()
        except Exception as e:
            print(f"Excepción en stop_threads: {e}")

if __name__ == '__main__':
    main()
