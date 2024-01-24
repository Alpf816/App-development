import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QGridLayout, QDockWidget, QMainWindow,QSlider
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt, QThread, QMutex, QTimer, pyqtSignal, QMutexLocker,pyqtSlot
import cv2

class VideoStreamThread(QThread):
    frame_actualizado = pyqtSignal(QImage)
    finalizado = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.capturando = False
        self.pausado = False
        self.latest_frame = None
        self.frame_lock = QMutex()

    def get_latest_frame(self):
        with QMutexLocker(self.frame_lock):
            return self.latest_frame.copy() if self.latest_frame is not None else None

    def run(self):
        self.capturando = True
        video_stream = cv2.VideoCapture(0)

        while self.capturando:
            if not self.pausado:
                ret, frame = video_stream.read()

                if not ret:
                    break

                frame_video_ventanacentral = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                with QMutexLocker(self.frame_lock):
                    self.latest_frame = frame_video_ventanacentral.copy()

                q_image = QImage(frame_video_ventanacentral.data, frame_video_ventanacentral.shape[1],
                                frame_video_ventanacentral.shape[0], frame_video_ventanacentral.strides[0],
                                QImage.Format.Format_RGB888)

                self.frame_actualizado.emit(q_image)

            QThread.msleep(60)

        video_stream.release()
        self.finalizado.emit()

    def detener_captura(self):
        self.capturando = False

    def pausar_captura(self):
        self.pausado = True

    def reanudar_captura(self):
        self.pausado = False
class VideoWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.label_video = QLabel(self)
        layout = QGridLayout(self)
        layout.addWidget(self.label_video)

    def actualizar_frame(self, q_image):
        pixmap = QPixmap.fromImage(q_image)
        margin = 18
        pixmap = pixmap.scaled(self.width() - margin, self.height() - margin, Qt.AspectRatioMode.KeepAspectRatio)
        self.label_video.setPixmap(pixmap)

class MiVentana(QWidget):
    def __init__(self, video_thread):
        super().__init__()
        self.hilo_video = video_thread
        self.video_widget = VideoWidget(self)
        self.hilo_video.frame_actualizado.connect(self.video_widget.actualizar_frame)
        self.hilo_video.finalizado.connect(self.hilo_finalizado)

        layout_principal = QGridLayout(self)
        boton_iniciar = QPushButton("Iniciar Captura", self)
        boton_detener = QPushButton("Detener Captura", self)
        boton_iniciar.clicked.connect(self.iniciar_captura)
        boton_detener.clicked.connect(self.detener_captura)

        layout_principal.addWidget(self.video_widget, 1, 1, 1, 2)
        layout_principal.addWidget(boton_iniciar, 2, 1, 1, 1)
        layout_principal.addWidget(boton_detener, 2, 2, 1, 1)

    def iniciar_captura(self):
        self.hilo_video.start()

    def detener_captura(self):
        self.hilo_video.detener_captura()

    def hilo_finalizado(self):
        print("Captura finalizada")

class MiDockWidget(QWidget):
    
    def __init__(self, video_thread):
        super().__init__()
        self.hilo_video = video_thread
        
        self.label2 = QLabel(self)  # Agregado
        self.label3 = QLabel(self)  # Agregado
        self.label4 = QLabel(self)  # Agregado

        layout_principalQD = QGridLayout(self)
        start_button = QPushButton("Iniciar Captura mascara", self)
        stop_button = QPushButton("Detener Captura mascara", self)
        

        layout_principalQD.addWidget(self.label2, 1, 1, 1, 1)  # Agregado
        layout_principalQD.addWidget(self.label3, 2, 1, 1, 1)  # Agregado
        layout_principalQD.addWidget(self.label4, 1, 2, 1, 1)  # Agregado

        layout_principalQD.addWidget(start_button, 4, 1, 1, 1)
        layout_principalQD.addWidget(stop_button, 4, 2, 1, 1)
        

        self.camera_thread = video_thread
        self.image_processor_thread = ImageProcessorThread(self.camera_thread.get_latest_frame)
        self.image_processor_thread.processed_frame_signal.connect(self.update_frame2)
        self.image_processor_thread.processed_frame_signal1.connect(self.update_frame3)
        self.image_processor_thread.processed_frame_signal2.connect(self.update_frame4)

        self.timer = QTimer(self)
        self.timer.start(60)

        stop_button.clicked.connect(self.pausar_actualizacion)
        start_button.clicked.connect(self.reanudar_actualizacion)
        
        start_button.clicked.connect(self.start_camera)
        self.margin_slider = QSlider(Qt.Orientation.Horizontal)
        self.margin_slider.setMinimum(200)
        self.margin_slider.setMaximum(400)
        self.margin_slider.setValue(200)  # Puedes establecer el valor inicial
        self.margin_slider.valueChanged.connect(self.actualizar_margin)

        layout_principalQD.addWidget(self.margin_slider, 3, 1, 1, 2)

    def actualizar_margin(self, value):
        # Esta función se ejecutará cuando cambie el valor del slider
        self.margin = value
        # Actualizar la variable margin en las funciones update_frame
        self.update_frame2(self.latest_image2)
        self.update_frame3(self.latest_image3)
        self.update_frame4(self.latest_image4)
        
        

    def update_frame2(self, image2):
        self.latest_image2 = image2
        margin = self.margin_slider.value()
        pixmap2 = QPixmap.fromImage(image2)
        pixmap2 = pixmap2.scaled(margin, margin, Qt.AspectRatioMode.KeepAspectRatio)
        self.label2.setPixmap(pixmap2)

    def update_frame3(self, image3):
        self.latest_image3 = image3
        margin = self.margin_slider.value()
        pixmap3 = QPixmap.fromImage(image3)
        pixmap3 = pixmap3.scaled(margin, margin, Qt.AspectRatioMode.KeepAspectRatio)
        self.label3.setPixmap(pixmap3)

    def update_frame4(self, image4):
        self.latest_image4 = image4
        margin = self.margin_slider.value()
        pixmap4 = QPixmap.fromImage(image4)
        
        pixmap4 = pixmap4.scaled(margin, margin, Qt.AspectRatioMode.KeepAspectRatio)
        self.label4.setPixmap(pixmap4)
    
    def start_camera(self):
        if not self.camera_thread.isRunning():
            self.camera_thread.start()
            self.image_processor_thread.start()

    def stop_camera(self):
        if self.camera_thread.isRunning():
            self.image_processor_thread.stop()
            self.clear_labels()

    def pausar_actualizacion(self):
        self.image_processor_thread.pausar()

    def reanudar_actualizacion(self):
        self.image_processor_thread.reanudar()

    def clear_labels(self):
        self.label2.clear()
        self.label3.clear()
        self.label4.clear()

    def closeEvent(self, event):
        self.stop_camera()
        event.accept()

class ImageProcessorThread(QThread):
    processed_frame_signal = pyqtSignal(QImage)
    processed_frame_signal1 = pyqtSignal(QImage)
    processed_frame_signal2 = pyqtSignal(QImage)

    pausar_signal = pyqtSignal()
    reanudar_signal = pyqtSignal()

    def __init__(self, get_frame_function):
        super().__init__()
        self.running = True
        self.paused = False
        self.get_frame_function = get_frame_function

    def run(self):
        while self.running:
            frame = self.get_frame_function()
            if frame is not None and frame.size != 0:
                if not self.paused:
                    qt_rgb_image = QImage(frame.data, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format.Format_RGB888)
                    self.processed_frame_signal.emit(qt_rgb_image)

                    gray_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
                    qt_gray_image = QImage(gray_frame.data, gray_frame.shape[1], gray_frame.shape[0], gray_frame.strides[0], QImage.Format.Format_Grayscale8)
                    self.processed_frame_signal1.emit(qt_gray_image)

                    modified_frame = cv2.applyColorMap(frame, cv2.COLORMAP_JET)
                    qt_modified_image = QImage(modified_frame.data, modified_frame.shape[1], modified_frame.shape[0], modified_frame.strides[0], QImage.Format.Format_RGB888)
                    self.processed_frame_signal2.emit(qt_modified_image)

                QThread.msleep(60)
            else:
                pass

    def stop(self):
        self.running = False
        self.wait()

    def pausar(self):
        self.pausar_signal.emit()

    def reanudar(self):
        self.reanudar_signal.emit()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Cámara con PyQt6 y OpenCV")
        self.setGeometry(100, 100, 1400, 750)
        
        video_thread = VideoStreamThread()

        ventana_video_principal = MiVentana(video_thread)
        midockwidget = MiDockWidget(video_thread)

        self.setCentralWidget(ventana_video_principal)
        self.dock2 = QDockWidget()
        self.dock2.setWidget(midockwidget)

        self.dock2.setWindowTitle("Mascara y Resultados")
        self.dock2.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock2)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    try:
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"Error: {e}")
