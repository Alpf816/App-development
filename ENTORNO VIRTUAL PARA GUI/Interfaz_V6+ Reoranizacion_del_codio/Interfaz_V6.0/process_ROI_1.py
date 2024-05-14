import sys
import cv2
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget
from PyQt6.QtGui import QImage, QPixmap
from multiprocessing import Process, Value, shared_memory, set_start_method

def frame_processor(shared_memory_name, frame_shape, running_flag):
    shm = shared_memory.SharedMemory(name=shared_memory_name)
    while running_flag.value:
        frame = shm.buf[:].reshape(frame_shape)
        # Aplicar algún filtro al frame (ejemplo: inversión de colores)
        processed_frame = cv2.bitwise_not(frame)
        # Actualizar el frame procesado en la memoria compartida
        shm.buf[:] = processed_frame.flatten()
    shm.close()

def video_capture(shared_memory_name, frame_shape, running_flag):
    cap = cv2.VideoCapture(0)
    shm = shared_memory.SharedMemory(name=shared_memory_name)
    while running_flag.value:
        ret, frame = cap.read()
        if ret:
            # Actualizar el frame capturado en la memoria compartida
            shm.buf[:] = frame.flatten()
    cap.release()
    shm.close()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.shared_memory_name = "shared_frame_memory"
        self.frame_shape = (480, 640, 3)
        self.running_flag = Value('b', False)

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.label = QLabel(self)
        layout.addWidget(self.label)

        start_button = QPushButton('Start', self)
        start_button.clicked.connect(self.start_processing)
        layout.addWidget(start_button)

        stop_button = QPushButton('Stop', self)
        stop_button.clicked.connect(self.stop_processing)
        layout.addWidget(stop_button)

        self.video_process = None
        self.processing_process = None

        self.show()

    def start_processing(self):
        self.running_flag.value = True

        # Crear la memoria compartida para los frames
        shm = shared_memory.SharedMemory(name=self.shared_memory_name, create=True, size=self.frame_shape[0] * self.frame_shape[1] * self.frame_shape[2])

        # Iniciar el proceso de captura de video
        self.video_process = Process(target=video_capture, args=(self.shared_memory_name, self.frame_shape, self.running_flag))
        self.video_process.start()

        # Iniciar el proceso de procesamiento de frames
        self.processing_process = Process(target=frame_processor, args=(self.shared_memory_name, self.frame_shape, self.running_flag))
        self.processing_process.start()

        self.update_label()

    def stop_processing(self):
        self.running_flag.value = False

        if self.video_process is not None:
            self.video_process.join()

        if self.processing_process is not None:
            self.processing_process.join()

        # Liberar la memoria compartida al detener la aplicación
        shared_memory.SharedMemory(name=self.shared_memory_name).close()
        shared_memory.SharedMemory(name=self.shared_memory_name).unlink()

    def update_label(self):
        shm = shared_memory.SharedMemory(name=self.shared_memory_name)
        while self.running_flag.value:
            frame = shm.buf[:].reshape(self.frame_shape)
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            qt_img = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_img)
            self.label.setPixmap(pixmap)
        shm.close()

    def closeEvent(self, event):
        self.stop_processing()
        event.accept()

if __name__ == '__main__':
    set_start_method('spawn')  # Configura el método de inicio del proceso
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
