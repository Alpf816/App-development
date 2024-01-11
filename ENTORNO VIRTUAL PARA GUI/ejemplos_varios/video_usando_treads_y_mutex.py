import sys
import cv2
from PyQt6.QtCore import Qt, QThread, QMutex, QMutexLocker, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget

class VideoThread(QThread):
    frame_updated = pyqtSignal(QImage)

    def __init__(self, mutex):
        super().__init__()
        self.mutex = mutex

    def run(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if ret:
                with QMutexLocker(self.mutex):
                    self.frame_updated.emit(self.convert_frame(frame))

    def convert_frame(self, frame):
        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        q_image = q_image.rgbSwapped()
        return q_image

class ModifiedVideoThread(QThread):
    frame_updated = pyqtSignal(QImage)

    def __init__(self, mutex):
        super().__init__()
        self.mutex = mutex
        self.frame = None

    def run(self):
        while True:
            with QMutexLocker(self.mutex):
                # Obtener una copia del frame del hilo principal
                frame_copy = self.frame.copy() if self.frame is not None else None

            # Verificar si se obtuvo un frame válido
            if frame_copy is not None:
                # Aplicar alguna modificación al frame aquí si es necesario

                # Emitir señal con el frame modificado
                self.frame_updated.emit(frame_copy)

    def set_frame(self, frame):
        # Método para establecer el frame desde el hilo principal
        self.frame = frame

class MainWindow(QWidget):
    def __init__(self, video_thread, modified_video_thread):
        super().__init__()

        self.video_label = QLabel()
        self.modified_video_label = QLabel()

        self.setup_ui()
        self.setup_threads(video_thread, modified_video_thread)

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self.video_label)
        layout.addWidget(self.modified_video_label)

    def setup_threads(self, video_thread, modified_video_thread):
        video_thread.frame_updated.connect(self.update_video_label)
        video_thread.start()

        modified_video_thread.frame_updated.connect(self.update_modified_video_label)
        modified_video_thread.start()

    def update_video_label(self, frame):
        pixmap = QPixmap.fromImage(frame)
        self.video_label.setPixmap(pixmap)

    def update_modified_video_label(self, frame):
        pixmap = QPixmap.fromImage(frame)
        self.modified_video_label.setPixmap(pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    mutex = QMutex()

    video_thread = VideoThread(mutex)
    modified_video_thread = ModifiedVideoThread(mutex)

    # Establecer una referencia al frame en el hilo principal
    video_thread.frame_updated.connect(lambda frame: modified_video_thread.set_frame(frame))

    main_window = MainWindow(video_thread, modified_video_thread)
    main_window.show()

    sys.exit(app.exec())
