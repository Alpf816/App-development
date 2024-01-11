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
                            QSlider)
from PyQt6.QtGui import * 
from PyQt6.QtCore import Qt,QThread, pyqtSignal, QMutex, QMutexLocker,QTimer,pyqtSignal
import cv2
from queue import Queue
import numpy as np



class VideoStreamThread(QThread):
    frame_actualizado = pyqtSignal(QImage)
    finalizado = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.capturando = False
        self.latest_frame = None
        self.frame_lock = QMutex()

    def get_latest_frame(self):
        with QMutexLocker(self.frame_lock):
            return self.latest_frame.copy() if self.latest_frame is not None else None


    def run(self):
        self.capturando = True
        video_stream = cv2.VideoCapture(0)  # Puedes ajustar el índice según tu configuración

        while self.capturando:
            ret, frame = video_stream.read()
            frame_video_ventanacentral = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            with QMutexLocker(self.frame_lock):
                    self.latest_frame = frame_video_ventanacentral.copy()
            q_image = QImage(frame_video_ventanacentral.data, frame_video_ventanacentral.shape[1], frame_video_ventanacentral.shape[0], frame.strides[0], QImage.Format.Format_RGB888)
            
            
            # Convierte el frame de OpenCV a QImage
            
            # Emite la señal con el frame actualizado
            self.frame_actualizado.emit(q_image)
            QThread.msleep(60)
            if not ret:
                break

        video_stream.release()
        self.finalizado.emit()
        

    def detener_captura(self):
        self.capturando = False


class VideoWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.label_video = QLabel(self)
        layout = QHBoxLayout(self)
        layout.addWidget(self.label_video)

    def actualizar_frame(self, q_image):
        pixmap = QPixmap.fromImage(q_image)
        margin = 18
        pixmap = pixmap.scaled(self.width() - margin, self.height() - margin, Qt.AspectRatioMode.KeepAspectRatio)

        self.label_video.setPixmap(pixmap)

class ImageProcessorThread(QThread):
    processed_frame_signal = pyqtSignal(QImage)
    processed_frame_signal1 = pyqtSignal(QImage)
    processed_frame_signal2 = pyqtSignal(QImage)

    def __init__(self, get_frame_function):
        super().__init__()
        self.running = True
        self.get_frame_function = get_frame_function

    def run(self):
        while self.running:
            frame = self.get_frame_function()
            if frame is not None:
                # Convertir la primera imagen a formato RGB
                

                # Emitir la señal con la primera imagen en formato RGB
                qt_rgb_image = QImage(frame.data, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format.Format_RGB888)
                self.processed_frame_signal.emit(qt_rgb_image)

                # Convertir la segunda imagen a escala de grises
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

                # Emitir la señal con la segunda imagen en formato escala de grises
                qt_gray_image = QImage(gray_frame.data, gray_frame.shape[1], gray_frame.shape[0], gray_frame.strides[0], QImage.Format.Format_Grayscale8)
                self.processed_frame_signal1.emit(qt_gray_image)

                # Aplicar una modificación adicional a la tercera imagen
                modified_frame = cv2.applyColorMap(frame, cv2.COLORMAP_JET)

                # Emitir la señal con la tercera imagen modificada
                qt_modified_image = QImage(modified_frame.data, modified_frame.shape[1], modified_frame.shape[0], modified_frame.strides[0], QImage.Format.Format_RGB888)
                self.processed_frame_signal2.emit(qt_modified_image)

                # Agregar una pausa para evitar saturar el hilo principal
                QThread.msleep(60)
            else:
                pass

    def stop(self):
        self.running = False
        self.wait()



class MiVentana(QWidget):
    def __init__(self):
        super().__init__()
        self.hilo_video = VideoStreamThread()
        self.video_widget = VideoWidget(self)
        self.hilo_video.frame_actualizado.connect(self.video_widget.actualizar_frame)
        self.hilo_video.finalizado.connect(self.hilo_finalizado)

        layout_principal = QGridLayout(self)
        boton_iniciar = QPushButton("Iniciar Captura", self)
        boton_detener = QPushButton("Detener Captura", self)
        boton_iniciar.clicked.connect(self.iniciar_captura)
        boton_detener.clicked.connect(self.detener_captura)



        layout_principal.addWidget(self.video_widget,1,1,1,2)
        layout_principal.addWidget(boton_iniciar,2,1,1,1)
        layout_principal.addWidget(boton_detener,2,2,1,1)


    
        
    def iniciar_captura(self):
        self.hilo_video.start()

    def detener_captura(self):
        self.hilo_video.detener_captura()

    def hilo_finalizado(self):
        print("Captura finalizada")
        # Realizar cualquier limpieza o acción necesaria al finalizar la captura
class MiDockWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.hilo_video = VideoStreamThread()
        # Crear widgets
        self.label = QLabel(self)
        self.label2 = QLabel(self)
        self.label3 = QLabel(self)  # Nueva QLabel para la segunda imagen procesada
        self.label4 = QLabel(self)  # Nueva QLabel para la tercera imagen procesada
        self.video_widget = VideoWidget(self)
        

        layout_principal = QGridLayout(self)
        start_button = QPushButton("Iniciar Captura mascara", self)
        stop_button = QPushButton("Detener Captura mascara", self)
        # Conectar botones a funciones
        start_button.clicked.connect(self.start_camera)
        stop_button.clicked.connect(self.stop_camera)

        # Layout
        layout = QGridLayout()
        layout.addWidget(self.label,0,1,1,3)
        layout.addWidget(self.label2,1,1,1,1)
        layout.addWidget(self.label3,1,2,1,1)
        layout.addWidget(self.label4,1,3,1,1)
        layout_principal.addWidget(self.video_widget,3,1,1,1)
        layout_principal.addWidget(start_button,4,1,1,1)
        layout_principal.addWidget(stop_button,4,2,1,1)
        # Inicializar variables
        self.camera_thread = VideoStreamThread()
        self.camera_thread.frame_actualizado.connect(self.update_frame)
        self.image_processor_thread = ImageProcessorThread(self.camera_thread.get_latest_frame)
        self.image_processor_thread.processed_frame_signal.connect(self.update_frame2)
        self.image_processor_thread.processed_frame_signal1.connect(self.update_frame3)
        self.image_processor_thread.processed_frame_signal2.connect(self.update_frame4)

        # Agregar un temporizador para controlar la velocidad de actualización de la interfaz
        self.timer = QTimer(self)
        
        self.timer.start(60)  # Establecer el intervalo del temporizador (en milisegundos)
    def start_camera(self):
        if not self.camera_thread.isRunning():
            self.camera_thread.start()
            self.image_processor_thread.start()

    def stop_camera(self):
        if self.camera_thread.isRunning():
            self.image_processor_thread.stop()
            self.clear_labels()

            
            

    def update_frame(self, image):
        pixmap = QPixmap.fromImage(image)
        self.label.setPixmap(pixmap)

    def update_frame2(self, image2):
        pixmap2 = QPixmap.fromImage(image2)
        self.label2.setPixmap(pixmap2)

    def update_frame3(self, image3):
        pixmap3 = QPixmap.fromImage(image3)
        self.label3.setPixmap(pixmap3)

    def update_frame4(self, image4):
        pixmap4 = QPixmap.fromImage(image4)
        self.label4.setPixmap(pixmap4)

    def clear_labels(self):
        # Limpiar los QLabel
        self.label2.clear()
        self.label3.clear()
        self.label4.clear()

    

                


    def closeEvent(self, event):
        # Detener los hilos al cerrar la aplicación
        self.stop_camera()
        event.accept()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Cámara con PyQt6 y OpenCV")
        ventana_video_principal = MiVentana()
        midockwidget = MiDockWidget()
        self.setCentralWidget(ventana_video_principal)
        self.dock2 = QDockWidget()
        self.dock2.setWidget(midockwidget)
        
        self.dock2.setWindowTitle("Mascara y Resultados")
        self.dock2.setAllowedAreas(
               Qt.DockWidgetArea.AllDockWidgetAreas
        )
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea,self.dock2)




if __name__ == "__main__":
    app = QApplication(sys.argv)

    try:
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"Error: {e}")