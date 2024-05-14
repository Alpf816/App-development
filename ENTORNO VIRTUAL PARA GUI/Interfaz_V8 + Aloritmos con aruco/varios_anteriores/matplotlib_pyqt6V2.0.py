import sys
import cv2
import multiprocessing
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton
import matplotlib.pyplot as plt


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()
        self.running = True

    def run(self):
        cap = cv2.VideoCapture(0)
        while self.running:
            ret, frame = cap.read()
            if ret:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_frame.shape
                bytes_per_line = ch * w
                convert_to_qt_format = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
                p = convert_to_qt_format.scaled(640, 480, Qt.AspectRatioMode.KeepAspectRatio)
                self.change_pixmap_signal.emit(p)
        cap.release()

    def stop(self):
        self.running = False
        self.wait()


class VideoWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video en Vivo")
        self.video_thread = VideoThread()
        self.image_label = QLabel(self)
        self.image_label.resize(640, 480)
        self.video_thread.change_pixmap_signal.connect(self.update_image)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.image_label)
        self.setLayout(main_layout)
        self.video_thread.start()

    def closeEvent(self, event):
        self.video_thread.stop()
        event.accept()

    def update_image(self, image):
        self.image_label.setPixmap(QPixmap.fromImage(image))


def run_matplotlib():
    x = [1, 2, 3, 4, 5]
    y = [1, 4, 9, 16, 25]

    plt.plot(x, y)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Matplotlib Example')
    plt.show()


def start_matplotlib_process():
    matplotlib_process = multiprocessing.Process(target=run_matplotlib)
    matplotlib_process.start()
    

def run_gui():
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("Video en Vivo")
    
    video_widget = VideoWidget()
    button = QPushButton("Mostrar Gráfico Matplotlib")
    button.clicked.connect(start_matplotlib_process)
    
    layout = QVBoxLayout()
    layout.addWidget(video_widget)
    layout.addWidget(button)
    
    window.setLayout(layout)
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    gui_process = multiprocessing.Process(target=run_gui)
    gui_process.start()
    gui_process.join()
