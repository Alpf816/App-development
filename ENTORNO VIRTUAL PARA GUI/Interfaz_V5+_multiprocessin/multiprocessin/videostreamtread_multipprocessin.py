import os
import psutil
import sys
from PyQt6.QtWidgets import (QApplication,
                            QWidget,
                            QLabel,
                            QLineEdit,
                            QPushButton,
                            QMessageBox,
                            QCheckBox,
                            QMainWindow,
                            QDockWidget,
                            QStatusBar,
                            QHBoxLayout,
                            QVBoxLayout,
                            QTabWidget,
                            QMainWindow,
                            QListWidget,
                            QGridLayout,
                            QFrame,
                            QSlider,
                            QComboBox,
                            QTableWidget,
                            QTableWidgetItem,
                            QScrollArea,
                            QSizePolicy)
from PyQt6.QtGui import QImage, QPixmap,QAction,QKeySequence,QIntValidator
from PyQt6.QtCore import Qt,QThread, pyqtSignal, QMutex, QMutexLocker,QTimer,QObject, pyqtSlot
import cv2
from queue import Queue
import numpy as np
import time
from multiprocessing import Process, Queue, Value, Manager

width_video_capture = 640
height_video_capture = 480



class ImageProcessor(Process):
    def __init__(self, input_queue, output_queue, slider_value,width_video_capture,height_video_capture):
        super().__init__()
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.slider_value = slider_value
        self.height_video_capture = height_video_capture
        self.width_video_capture = width_video_capture
        

    def run(self):
        coordinate_image_initialized = False
        while True:
            try:
                frame = self.input_queue.get()  # Espera a recibir un frame desde el hilo principal
                roi_x, roi_y, roi_width, roi_height = 100, 100, 200, 200

                if not coordinate_image_initialized:
                    coordinate_image = self.create_cartesian_plane_custom(width_video_capture, height_video_capture, 50, 0, 0)
                    coordinate_image_initialized = True
                    print("se actualizo el plano")
                frame_video_ventanacentral = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                cv2.rectangle(frame_video_ventanacentral, (roi_x+self.slider_value.value, roi_y), (roi_x + roi_width, roi_y + roi_height), (0, 255, 0), 2)
                combined_image = self.overlay_images(frame_video_ventanacentral, coordinate_image)

                # Ajusta el brillo de la imagen según el valor del slider
                
                print(self.slider_value.value)

                # Coloca el frame procesado en la cola de salida
                self.output_queue.put(combined_image)
            except Exception as e:
                print(f"Excepción en el hilo de ejecución: {e}")

    def create_cartesian_plane_custom(self, roi_width, roi_height, scale, Inicio_px_X, Inicio_px_Y):
        # Calcula las dimensiones del plano cartesiano según las dimensiones de la ROI
        width = roi_width
        height = roi_height
        image = np.zeros((height, width, 3), dtype=np.uint8)

        # Dibuja los ejes X e Y
        cv2.line(image, (0, height - 1), (width - 1, height - 1), (255, 0, 0), 2)
        cv2.line(image, (0, 0), (0, height - 1), (255, 0, 0), 2)

        # Dibuja las marcas cada `scale` píxeles en los ejes y las etiquetas con las coordenadas
        for x in range(0, width, scale):
            cv2.line(image, (x, height - 6), (x, height - 1), (255, 0, 0), 2)
            cv2.putText(image, str(x + Inicio_px_X), (x, height - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

        for y in range(0, height, scale):
            cv2.line(image, (0, height - y), (5, height - y), (255, 0, 0), 2)
            cv2.putText(image, str(y + Inicio_px_Y), (8, height - y + 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

        return image

    def overlay_images(self, background, overlay):
        # Asegúrate de que las imágenes tengan el mismo tamaño
        overlay = cv2.resize(overlay, (background.shape[1], background.shape[0]))

        # Si las imágenes tienen diferentes canales, convierte a escala de grises
        if overlay.shape[-1] != background.shape[-1]:
            overlay = cv2.cvtColor(overlay, cv2.COLOR_BGR2GRAY)

        # Combina las imágenes
        result = cv2.addWeighted(background, 1, overlay, 1, 0)

        return result
    

class ImageThread(QThread):
    frame_actualizado = pyqtSignal(QImage)
    frame_captured = pyqtSignal(np.ndarray)
    
    def __init__(self, input_queue, output_queue):
        super().__init__()
        print("Initializing ImageThread")
        self.input_queue = input_queue
        self.latest_frame = None
        self.frame_lock = QMutex()
        
        self.video_stream = cv2.VideoCapture(0)  # Puedes ajustar el número de la cámara según tus necesidades
    
        
        width_video_capture = int(self.video_stream.get(cv2.CAP_PROP_FRAME_WIDTH))
        height_video_capture = int(self.video_stream.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print(f"Resolución de la cámara: {width_video_capture}x{height_video_capture}")
            
    def get_latest_frame(self):
        with QMutexLocker(self.frame_lock):
            return self.latest_frame if self.latest_frame is not None else None

    def run(self):
        try:
            while True:
                ret, frame = self.video_stream.read()
                if not ret:
                    raise Exception(f"Error al capturar el fotograma: {width_video_capture} x {height_video_capture}")
                
                with QMutexLocker(self.frame_lock):
                    self.latest_frame = frame
                    # print("frame copiado y enviado")

                # Emitir la señal con el frame capturado
                self.frame_captured.emit(frame)

        except Exception as e:
            print(f"Excepción en el hilo de ejecución: {e}")
        finally:
            self.video_stream.release()
            # self.finalizado.emit()


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
        self.image_thread = ImageThread(self.input_queue, self.output_queue)
        self.image_thread.frame_captured.connect(self.process_frame)
        self.image_thread.start()

        width_video_capture = self.image_thread.video_stream.get(cv2.CAP_PROP_FRAME_WIDTH)
        height_video_capture = self.image_thread.video_stream.get(cv2.CAP_PROP_FRAME_HEIGHT)

        self.image_processor = ImageProcessor(self.input_queue, self.output_queue, self.slider_value, width_video_capture, height_video_capture)
        self.image_processor.start()

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
    def update_image(self, combined_image):
        # Convierte la imagen de OpenCV a QImage y muestra en el QLabel
        q_image = QImage(combined_image.data, width_video_capture, height_video_capture, width_video_capture * 3, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        self.label.setPixmap(pixmap)

    def closeEvent(self, event):
        # Detiene el proceso de procesamiento de imágenes antes de cerrar la aplicación
        self.image_processor.terminate()
        self.image_thread.terminate()
        
        # Libera la cámara
        cv2.VideoCapture(0).release()
        
        event.accept()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
