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
from PyQt6.QtCore import Qt,QThread, pyqtSignal, QMutex, QMutexLocker,QTimer,QObject, pyqtSlot,QCoreApplication
import cv2
from queue import Queue
import numpy as np
import time
from multiprocessing import Process, Queue, Value, Manager,Event
width_video_capture = 640
height_video_capture = 480



class ImageProcessor(Process):
    
    def __init__(self, input_queue, output_queue, slider_value, width_video_capture, height_video_capture):
        super().__init__()
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.slider_value = slider_value
        self.height_video_capture = height_video_capture
        self.width_video_capture = width_video_capture
        self.terminate_flag = False
        print("Se Init Proceso")

    def run(self):
            
            coordinate_image_initialized = False

            while True:
                try:
                    frame = self.input_queue.get(block=True)
                    roi_x, roi_y, roi_width, roi_height = 100, 100, 200, 200

                    if not coordinate_image_initialized:
                        coordinate_image = self.create_cartesian_plane_custom(
                            self.width_video_capture, self.height_video_capture, 50, 0, 0
                        )
                        coordinate_image_initialized = True
                        print("Se actualizó el plano")

                    frame_video_ventanacentral = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    cv2.rectangle(
                        frame_video_ventanacentral,
                        (roi_x + self.slider_value.value, roi_y),
                        (roi_x + roi_width, roi_y + roi_height),
                        (0, 255, 0),
                        2,
                    )
                    mascara2 = cv2.inRange(frame_video_ventanacentral, (0,0,0),(100,100,100))
                    kernel2 = np.ones((5,5), np.uint8)
                    mascara2 = cv2.morphologyEx(mascara2, cv2.MORPH_CLOSE, kernel2)
                    mascara2 = cv2.morphologyEx(mascara2, cv2.MORPH_OPEN, kernel2)
                    contorno2, _ = cv2.findContours(mascara2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    contour_image2 = np.zeros((frame.shape[0], frame.shape[1], 3), dtype=np.uint8)
                    if contorno2:
                        cv2.drawContours(contour_image2, contorno2, -1, (0, 255, 0), 2)
                        if contour_image2 is not None and contour_image2.shape[0] > 0 and contour_image2.shape[1] > 0:
            
                            combined_image = self.overlay_images(
                                contour_image2, coordinate_image
                            )

                    self.output_queue.put(combined_image)
                except Exception as e:
                    print(f"Excepción en el hilo de ejecución: {e}")
                if self.terminate_flag:
                    print("Process terminated.")
                    break
        #self.main_window.process_finished_handler()
    def terminate_process(self):
        self.terminate_flag = True
            

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
            cv2.line(image, (x, 0), (x, 6), (255, 0, 0), 2)
            cv2.putText(image, str(x + Inicio_px_X), (x, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

        for y in range(0, height, scale):
            cv2.line(image, (0, y), (5, y), (255, 0, 0), 2)
            cv2.putText(image, str(y + Inicio_px_Y), (8, y + 5),
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
    process_finished = pyqtSignal()

    def __init__(self, input_queue, output_queues):
        super().__init__()
        print("Initializing ImageThread")
        #self.input_queue = input_queue
        self.latest_frame = None
        self.frame_lock = QMutex()
        #self.output_queues = output_queues  # Almacena las colas de salida
        self.image_processors = []  # Lista para mantener instancias de ImageProcessor

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

                self.frame_captured.emit(frame)

        except Exception as e:
            print(f"Excepción en el hilo de ejecución: {e}")
        finally:
            self.video_stream.release()
            self.process_finished.emit()  # Emite la señal de finalización

    
    def __del__(self):
        # Libera la cámara al destruir la instancia
        if self.video_stream.isOpened():
            self.video_stream.release()
        
    def stop_processing(self):
        # Detener la captura de frames
        self.terminate()
        self.wait()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Bandera de señal de detención para los procesos
        self.input_queue = Queue()
        self.output_queues = []  # Lista de colas de salida para cada ImageProcessor
        self.slider_value = Value('i', 0)
        
        self.labels = []  # Lista de QLabel asociados a cada ImageProcessor
        self.image_processors = []  # Lista para mantener instancias de ImageProcessor

        self.setup_ui()
        self.image_thread = ImageThread(self.input_queue, self.output_queues)

        self.image_thread.frame_captured.connect(self.process_frame)
        self.image_thread.process_finished.connect(self.process_finished_handler)  # Conecta la señal de finalización

        # Inicia el proceso de procesamiento de imágenes


        self.image_thread.start()
        
        

        # Inicia el proceso de procesamiento de imágenes

    def setup_ui(self):
        global width_video_capture,height_video_capture

        # Crear un QVBoxLayout principal para organizar los QLabel
        layout = QVBoxLayout()
        self.label = QLabel(self)
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(0)
        self.slider.setSingleStep(10)
        self.stop_button = QPushButton("Detener Procesos", self)
        self.stop_button.clicked.connect(self.detener_procesos)

        # Inicia múltiples ImageProcessor
        num_processors = 3  # Puedes ajustar la cantidad según tus necesidades
        for i in range(num_processors):
            output_queue = Queue()
            self.output_queues.append(output_queue)

            processor = ImageProcessor(self.input_queue, output_queue, self.slider_value, width_video_capture, height_video_capture)
            processor.start()

            # Crea QLabel para mostrar el resultado de cada ImageProcessor y enuméralos
            label = QLabel(self)
            label.setText(f"Resultado del ImageProcessor {i + 1}")
            self.labels.append(label)
            # Agrega cada QLabel al QVBoxLayout principal
            layout.addWidget(label)

        
        layout.addWidget(self.label)
        layout.addWidget(self.slider)
        layout.addWidget(self.stop_button)

        self.setLayout(layout)

        self.setWindowTitle("OpenCV y PyQt6")

        # Conecta la señal del slider directamente al método de actualización
        self.slider.valueChanged.connect(self.update_slider_value)

        # Configura un temporizador para actualizar la GUI
        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: self.update_gui())
        self.timer.start(50)



        #width_video_capture = self.image_thread.video_stream.get(cv2.CAP_PROP_FRAME_WIDTH)
        #height_video_capture = self.image_thread.video_stream.get(cv2.CAP_PROP_FRAME_HEIGHT)


    #@pyqtSlot(np.ndarray)
    def process_frame(self, frame):
        # Pasa el frame al proceso de procesamiento
        self.input_queue.put(frame)
        # Almacena las instancias de ImageProcessor
        #self.image_processors = [p for p in self.image_processors if p.is_alive()] es necesario????

    def update_slider_value(self, value):
        # Actualiza el valor del slider y envía el nuevo valor al proceso de procesamiento
        self.slider_value.value = value

    #@pyqtSlot(np.ndarray)
    def update_gui(self):
    # Revisa todas las colas de salida y actualiza la GUI para cada ImageProcessor
        for i, output_queue in enumerate(self.output_queues):
            if isinstance(output_queue, type(Queue())):
                while not output_queue.empty():
                    processed_frame = output_queue.get()
                    self.update_image(processed_frame, i)
                                        
    def update_image(self, combined_image, index):
        # Convierte la imagen de OpenCV a QImage y muestra en el QLabel correspondiente
        q_image = QImage(combined_image.data, width_video_capture, height_video_capture, width_video_capture * 3, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        self.labels[index].setPixmap(pixmap)

    def closeEvent(self, event):
        try:
            print("Closing application...")
            self.detener_procesos()  # Llama a la función para detener procesos

            if self.image_thread.video_stream.isOpened():
                self.image_thread.video_stream.release()
            self.cleanup()
            print("Application closed.")
            event.accept()
        except Exception as e:
            print(f"Excepción en el hilo de ejecución: {e}")
        finally:
            print("Se finalizó el Programa")

        
        
    def process_finished_handler(self):
        print("ImageThread has finished.")
        for processor in self.image_processors:
            processor.terminate_process()

    def cleanup(self):
        # Limpiar y cerrar recursos
        self.input_queue.close()
        self.input_queue.join_thread()

        for processor in self.image_processors:
            processor.join()

        self.image_thread.quit()
        self.image_thread.wait()
        QCoreApplication.instance().quit()
        print("Se cerró el thread!")

    def detener_procesos(self):
        print("Deteniendo procesos...")
        for processor in self.image_processors:
            processor.terminate_process()

        # Puedes esperar a que los procesos terminen si es necesario
        # for processor in self.image_processors:
        #     processor.join()

        print("Procesos detenidos.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
