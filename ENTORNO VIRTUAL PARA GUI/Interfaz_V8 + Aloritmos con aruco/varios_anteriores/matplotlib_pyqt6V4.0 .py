import sys
import cv2
import multiprocessing
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

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


class matplotlib_process(multiprocessing.Process):
    def __init__(self, flag):
        super().__init__()
        self.process_flag_interno = flag

    def run(self):
        # Creamos la figura y los ejes 3D
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Inicialización del gráfico
        def init():
            ax.set_xlim(-1, 1)
            ax.set_ylim(-1, 1)
            ax.set_zlim(0, 2*np.pi)
            return ax,

        # Definimos la función de actualización para recibir nuevos datos
        def update(data):
            x, y, z = data  # Desempaquetamos los datos
            ax.clear()
            ax.plot(x, y, z)
            ax.set_xlim(-1, 1)
            ax.set_ylim(-1, 1)
            ax.set_zlim(0, 2*np.pi)
            return ax,

        # Creamos una función para recibir datos nuevos
        def new_data():
            while self.process_flag_interno.value:
                # Simulamos la recepción de datos en tiempo real
                x = np.random.uniform(-1, 1, 100)
                y = np.random.uniform(-1, 1, 100)
                z = np.linspace(0, 2*np.pi, 100)
                yield x, y, z

        # Creamos la animación que se actualiza con nuevos datos
        ani = FuncAnimation(fig, update, frames=new_data, init_func=init, blit=True, interval=200, save_count=100)

        # Mostramos la animación
        plt.show()


def close_matplotlib_process(matplotlib_process_inst, flag):
    flag.value = False
    if matplotlib_process_inst.is_alive():
        matplotlib_process_inst.terminate()


def start_matplotlib_process(matplotlib_process_inst,flag):
    
    matplotlib_process_inst.start()


def run_gui():
    
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("Video en Vivo")

    flag = multiprocessing.Value('b', True)
    matplotlib_process_inst = matplotlib_process(flag)
    video_widget = VideoWidget()
    button = QPushButton("Mostrar Gráfico Matplotlib")
    button.clicked.connect(lambda: start_matplotlib_process(matplotlib_process_inst, flag))
    close_button = QPushButton("Cerrar Gráfico Matplotlib")
    close_button.clicked.connect(lambda: close_matplotlib_process(matplotlib_process_inst, flag))

    layout = QVBoxLayout()
    layout.addWidget(video_widget)
    layout.addWidget(button)
    layout.addWidget(close_button)

    window.setLayout(layout)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    run_gui()
