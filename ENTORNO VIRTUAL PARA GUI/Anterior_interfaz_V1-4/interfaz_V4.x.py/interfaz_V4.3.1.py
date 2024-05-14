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
from PyQt6.QtCore import Qt,QThread, pyqtSignal, QMutex, QMutexLocker,QTimer,QObject
import cv2
from queue import Queue
import numpy as np
import time

width_video_capture = int
height_video_capture = int


class VideoStreamThread(QThread):
    frame_actualizado = pyqtSignal(QImage)
    finalizado = pyqtSignal()
    data_updated = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.capturando = False
        self.pausado = False
        self.latest_frame = None
        self.frame_lock = QMutex()
        self.parameters_values = {}
        

    def get_latest_frame(self):
        with QMutexLocker(self.frame_lock):
            return self.latest_frame.copy() if self.latest_frame is not None else None

    def run(self):
        try:
            coordinate_image_initialized = False
            coordinate_image = None
            Yatenodatos = True
            self.capturando = True
            video_stream = cv2.VideoCapture(0)
            if Yatenodatos:
                global width_video_capture, height_video_capture
                width_video_capture = int(video_stream.get(cv2.CAP_PROP_FRAME_WIDTH))
                height_video_capture = int(video_stream.get(cv2.CAP_PROP_FRAME_HEIGHT))
                Yatenodatos = False
            print(f"Resolución de la cámara: {width_video_capture}x{height_video_capture}")

            while self.capturando:
                if not self.pausado:
                    inicio_iteracion = time.time()
                    ret, frame = video_stream.read()

                    if not ret:
                        raise Exception(f"Error al capturar el fotograma: {video_stream.get(cv2.CAP_PROP_FRAME_WIDTH)} x {video_stream.get(cv2.CAP_PROP_FRAME_HEIGHT)}")

                    with QMutexLocker(self.frame_lock):
                        self.latest_frame = frame.copy()

                    roi_x, roi_y, roi_width, roi_height = 0, 0, 400, 400

                    if not coordinate_image_initialized:
                        coordinate_image = self.create_cartesian_plane_custom(width_video_capture, height_video_capture, 50, 0, 0)
                        coordinate_image_initialized = True
                    frame_video_ventanacentral = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    cv2.rectangle(frame_video_ventanacentral, (roi_x, roi_y), (roi_x + roi_width, roi_y + roi_height), (0, 255, 0), 2)
                    combined_image = self.overlay_images(frame_video_ventanacentral, coordinate_image)

                    q_image = QImage(combined_image.data, width_video_capture, height_video_capture, width_video_capture * 3, QImage.Format.Format_RGB888)

                    self.frame_actualizado.emit(q_image)

                    fin_iteracion = time.time()
                    

                QThread.msleep(60)
                duracion_iteracion = fin_iteracion - inicio_iteracion
                tasa_de_fps_aprox = 1/duracion_iteracion
                print(f'tasa de fps aprox: {tasa_de_fps_aprox} fps')

        except Exception as e:
            print(f"Excepción en el hilo de ejecución: {e}")

        finally:
            video_stream.release()
            self.finalizado.emit()
    
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

    def detener_captura(self):
        self.capturando = False

    def pausar_captura(self):
        self.pausado = True

    def reanudar_captura(self):
        self.pausado = False
class VideoWidget(QWidget):
    def __init__(self ):
        super().__init__()
        try:
            int_validator = QIntValidator()
            
            self.label_video = QLabel(self)
            layout = QGridLayout(self)
            self.edit_text1 = QLineEdit(self)
            self.edit_text2 = QLineEdit(self)
            self.edit_text3 = QLineEdit(self)
            self.edit_text4 = QLineEdit(self)
            self.edit_text5 = QLineEdit(self)
            self.edit_text6 = QLineEdit(self)
            self.edit_text7 = QLineEdit(self)
            self.edit_text8 = QLineEdit(self)
            
            self.edit_text1.setValidator(int_validator)
            self.edit_text2.setValidator(int_validator)
            self.edit_text3.setValidator(int_validator)
            self.edit_text4.setValidator(int_validator)
            self.edit_text5.setValidator(int_validator)
            self.edit_text6.setValidator(int_validator)
            self.edit_text7.setValidator(int_validator)
            self.edit_text8.setValidator(int_validator)
            
            # Add labels for QLineEdit widgets
            label1 = QLabel("Text 1:", self)
            label2 = QLabel("Text 2:", self)
            label3 = QLabel("Text 3:", self)
            label4 = QLabel("Text 4:", self)
            label5 = QLabel("Text 5:", self)
            label6 = QLabel("Text 6:", self)
            label7 = QLabel("Text 7:", self)
            label8 = QLabel("Text 8:", self)
            
            for edit_widget in [self.edit_text1, self.edit_text2, self.edit_text3, self.edit_text4,
                                self.edit_text5, self.edit_text6, self.edit_text7, self.edit_text8]:
                edit_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            # Set up the layout
            layout.addWidget(label1, 0, 0)
            layout.addWidget(self.edit_text1, 0, 1)
            layout.addWidget(label2, 1, 0)
            layout.addWidget(self.edit_text2, 1, 1)
            layout.addWidget(label3, 0, 2)
            layout.addWidget(self.edit_text3, 0, 3)
            layout.addWidget(label4, 1, 2)
            layout.addWidget(self.edit_text4, 1, 3)
            layout.addWidget(label5, 0, 4)
            layout.addWidget(self.edit_text5, 0, 5)
            layout.addWidget(label6, 1, 4)
            layout.addWidget(self.edit_text6, 1, 5)
            layout.addWidget(label7, 0, 6)
            layout.addWidget(self.edit_text7, 0, 7)
            layout.addWidget(label8, 1, 6)
            layout.addWidget(self.edit_text8, 1, 7)
            layout.addWidget(self.label_video, 5,0,1,8)  # Adjust the row span for the video label

            
            
            self.edit_text1.textChanged.connect(self.on_text_changed)
            self.edit_text2.textChanged.connect(self.on_text_changed)
            self.edit_text3.textChanged.connect(self.on_text_changed)
            self.edit_text4.textChanged.connect(self.on_text_changed)
            self.edit_text5.textChanged.connect(self.on_text_changed)
            self.edit_text6.textChanged.connect(self.on_text_changed)
            self.edit_text7.textChanged.connect(self.on_text_changed)
            self.edit_text8.textChanged.connect(self.on_text_changed)


            
        except Exception as e:
            print(f"Error: {e}")
            
    def on_text_changed(self):
        text1 = int(self.edit_text1.text()) if self.edit_text1.text() else 0
        text2 = int(self.edit_text2.text()) if self.edit_text2.text() else 0
        text3 = int(self.edit_text3.text()) if self.edit_text3.text() else 0
        text4 = int(self.edit_text4.text()) if self.edit_text4.text() else 0
        text5 = int(self.edit_text5.text()) if self.edit_text5.text() else 0
        text6 = int(self.edit_text6.text()) if self.edit_text6.text() else 0
        text7 = int(self.edit_text7.text()) if self.edit_text7.text() else 0
        text8 = int(self.edit_text8.text()) if self.edit_text8.text() else 0
        a = {text1,text2,text3,text4,text5,text6,text7,text8}

            


        # Emit the signal with the updated text
        
        
        


    def actualizar_frame(self, q_image):
        try:
                
            if q_image:
                pixmap = QPixmap.fromImage(q_image)
                margin = 18
                pixmap = pixmap.scaled(self.width() - margin, self.height() - margin, Qt.AspectRatioMode.KeepAspectRatio)
                self.label_video.setPixmap(pixmap)
        except Exception as e:
            print(f"Excepción en el hilo de ejecución: {e}")
        

   

        

class MiVentana(QWidget):
    def __init__(self, video_thread):
        super().__init__()
        self.hilo_video = video_thread
        self.video_widget = VideoWidget()
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
    def __init__(self, video_thread,dic_thread):
        super().__init__()
        self.dic_thread = dic_thread
        self.hilo_video = video_thread
        self.presets_combobox = QComboBox(self)
        self.presets_combobox.addItems(["Original", "Seleccion de colores", "Contornos"])
        self.presets_combobox.currentIndexChanged.connect(self.on_preset_changed)
        # Crear instancia de ImageProcessorThread y pasarla a MiDockWidget
        self.image_processor_thread = ImageProcessorThread(self.hilo_video.get_latest_frame,self.dic_thread)
        
        self.label2 = QLabel(self)
        self.label3 = QLabel(self)
        self.label4 = QLabel(self)
        self.label5 = QLabel(self)

        layout_principalQD = QGridLayout(self)
        start_button = QPushButton("Iniciar Captura mascara", self)
        stop_button = QPushButton("Detener Captura mascara", self)

        layout_principalQD.addWidget(self.label2, 1, 1, 1, 1)
        layout_principalQD.addWidget(self.label3, 2, 1, 1, 1)
        layout_principalQD.addWidget(self.label4, 1, 2, 1, 1)
        layout_principalQD.addWidget(self.label5, 2, 2, 1, 1)

        layout_principalQD.addWidget(start_button, 4, 1, 1, 1)
        layout_principalQD.addWidget(stop_button, 4, 2, 1, 1)
        layout_principalQD.addWidget(self.presets_combobox, 5, 1, 1, 2)

        self.image_processor_thread.processed_frame_signal.connect(self.update_frame2)
        self.image_processor_thread.processed_frame_signal1.connect(self.update_frame3)
        self.image_processor_thread.processed_frame_signal2.connect(self.update_frame4)
        self.image_processor_thread.processed_frame_signal3.connect(self.update_frame5)

        self.timer = QTimer(self)
        self.timer.start(60)

        stop_button.clicked.connect(self.pausar_actualizacion)
        start_button.clicked.connect(self.reanudar_actualizacion)

        start_button.clicked.connect(self.start_camera)
        self.margin_slider = QSlider(Qt.Orientation.Horizontal)
        self.margin_slider.setMinimum(200)
        self.margin_slider.setMaximum(360)
        self.margin_slider.setValue(200)
        self.margin_slider.setSingleStep(5)
        self.margin_value = 200
        self.margin_slider.valueChanged.connect(self.actualizar_margin)

        layout_principalQD.addWidget(self.margin_slider, 3, 1, 1, 2)

    def on_preset_changed(self, index):
        # Obtener el valor seleccionado en el QComboBox y pasarlo al hilo de procesamiento de imágenes
        selected_preset = self.presets_combobox.itemText(index)
        self.image_processor_thread.set_selected_preset(selected_preset)
    def actualizar_margin(self, value):
        self.margin_value = value
        self.update_frame2()
        self.update_frame3()
        self.update_frame4()
        self.update_frame5()

    def update_frame2(self, image2=None):
        if image2 is not None:
            pixmap2 = QPixmap.fromImage(image2)
            pixmap2 = pixmap2.scaledToWidth(self.margin_value)
            self.label2.setPixmap(pixmap2)

    def update_frame3(self, image3=None):
        if image3 is not None:
            pixmap3 = QPixmap.fromImage(image3)
            pixmap3 = pixmap3.scaledToWidth(self.margin_value)
            self.label3.setPixmap(pixmap3)

    def update_frame4(self, image4=None):
        if image4 is not None:
            pixmap4 = QPixmap.fromImage(image4)
            pixmap4 = pixmap4.scaledToWidth(self.margin_value)
            self.label4.setPixmap(pixmap4)

    def update_frame5(self, image5=None):
        if image5 is not None:
            pixmap5 = QPixmap.fromImage(image5)
            pixmap5 = pixmap5.scaledToWidth(self.margin_value)
            self.label5.setPixmap(pixmap5)

    def start_camera(self):
        if not self.hilo_video.isRunning():
            self.hilo_video.start()
            self.image_processor_thread.start()

    def stop_camera(self):
        if self.hilo_video.isRunning():
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
    processed_frame_signal3 = pyqtSignal(QImage)
    pausar_signal = pyqtSignal()
    reanudar_signal = pyqtSignal()
    diccionario_del_IPT = dict
    TonMin1 = 1
    TonMax1 = 1
    PurMin1 = 1
    PurMax1 = 1
    LumMin1 = 1
    LumMax1 = 1
    KerX1 = 1
    KerY1 = 1
    TonMin2 = 1
    TonMax2 = 1
    PurMin2 = 1
    PurMax2 = 1
    LumMin2 = 1
    LumMax2 = 1
    KerX2 = 1
    KerY2 = 1
    TonMin3 = 1
    TonMax3 = 1
    PurMin3 = 1
    PurMax3 = 1
    LumMin3 = 1
    LumMax3 = 1
    KerX3 = 1
    KerY3 = 1
    TonMin4 = 1
    TonMax4 = 1
    PurMin4 = 1
    PurMax4 = 1
    LumMin4 = 1
    LumMax4 = 1
    KerX4 = 1
    KerY4 = 1

    def __init__(self, get_frame_function, dic_thread):
        super().__init__()
        self.running = True
        self.paused = False
        self.dic_thread = dic_thread
        self.dic_thread.enviar_signal.connect(self.actualizar_dic_IPT)
        self.get_frame_function = get_frame_function
        

        # Inicializar el preset actual
        self.current_preset = "Original"

    
##########################################################################aqui se conectan los sliders

    def run(self):
        while self.running:
            frame = self.get_frame_function()
            if frame is not None and frame.size != 0:
                if not self.paused:
                    if self.current_preset == "Original":
                        
                        qt_image_1 = QImage(frame.data, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format.Format_BGR888)
                        self.processed_frame_signal.emit(qt_image_1)

                        qt_image_2 = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
                        qt_image_2 = QImage(qt_image_2.data, qt_image_2.shape[1], qt_image_2.shape[0], qt_image_2.strides[0], QImage.Format.Format_Grayscale8)
                        self.processed_frame_signal1.emit(qt_image_2)

                        qt_image_3 = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
                        qt_image_3 = QImage(qt_image_3.data, qt_image_3.shape[1], qt_image_3.shape[0], qt_image_3.strides[0], QImage.Format.Format_Grayscale8)
                        self.processed_frame_signal2.emit(qt_image_3)
                        
                    
                        qt_image_4 = cv2.applyColorMap(frame, cv2.COLORMAP_JET)
                        qt_image_4 = QImage(qt_image_4.data, qt_image_4.shape[1], qt_image_4.shape[0], qt_image_4.strides[0], QImage.Format.Format_RGB888)
                        self.processed_frame_signal3.emit(qt_image_4)

                    elif self.current_preset == "Seleccion de colores":
                        pass
                        

                    elif self.current_preset == "Contornos":
                        #Color1-------------------------------------------
                        hsv1 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                        color_oscuro1 = np.array([self.TonMin1, self.PurMin1, self.LumMin1])
                        color_claro1 = np.array([self.TonMax1, self.PurMax1, self.LumMax1])
                        mascara1 = cv2.inRange(hsv1, color_oscuro1, color_claro1)
                        #if isinstance(self.KerX1, int) and isinstance(self.KerY1, int):
                        #    kernel1 = np.ones((self.KerX1, self.KerY1), np.uint8)
                        #mascara1 = cv2.morphologyEx(mascara1, cv2.MORPH_CLOSE, kernel1)
                        #mascara1 = cv2.morphologyEx(mascara1, cv2.MORPH_OPEN, kernel1)
                        contorno1, _ = cv2.findContours(mascara1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                        contour_image1 = np.zeros((frame.shape[0], frame.shape[1], 3), dtype=np.uint8)
                        if contorno1:
                            cv2.drawContours(contour_image1, contorno1, -1, (0, 255, 0), 2)
                            if contour_image1 is not None and contour_image1.shape[0] > 0 and contour_image1.shape[1] > 0:
                                qt_image_contour1 = QImage(contour_image1.data, contour_image1.shape[1], contour_image1.shape[0], contour_image1.strides[0], QImage.Format.Format_RGB888)
                                self.processed_frame_signal.emit(qt_image_contour1)

                        #Color2-------------------------------------------
                        hsv2 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                        color_oscuro2 = np.array([self.TonMin2, self.PurMin2, self.LumMin2])
                        color_claro2 = np.array([self.TonMax2, self.PurMax2, self.LumMax2])
                        mascara2 = cv2.inRange(hsv2, color_oscuro2, color_claro2)
                        #if isinstance(self.KerX2, int) and isinstance(self.KerY2, int):
                        #    kernel2 = np.ones((self.KerX2, self.KerY2), np.uint8)
                        #mascara2 = cv2.morphologyEx(mascara2, cv2.MORPH_CLOSE, kernel2)
                        #mascara2 = cv2.morphologyEx(mascara2, cv2.MORPH_OPEN, kernel2)
                        contorno2, _ = cv2.findContours(mascara2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                        contour_image2 = np.zeros((frame.shape[0], frame.shape[1], 3), dtype=np.uint8)
                        if contorno2:
                            cv2.drawContours(contour_image2, contorno2, -1, (0, 255, 0), 2)
                            if contour_image2 is not None and contour_image2.shape[0] > 0 and contour_image2.shape[1] > 0:
                                qt_image_contour2 = QImage(contour_image2.data, contour_image2.shape[1], contour_image2.shape[0], contour_image2.strides[0], QImage.Format.Format_RGB888)
                                self.processed_frame_signal1.emit(qt_image_contour2)
                        #Color3-------------------------------------------
                        hsv3 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                        color_oscuro3 = np.array([self.TonMin3, self.PurMin3, self.LumMin3])
                        color_claro3 = np.array([self.TonMax3, self.PurMax3, self.LumMax3])
                        mascara3 = cv2.inRange(hsv3, color_oscuro3, color_claro3)
                        #if isinstance(self.KerX3, int) and isinstance(self.KerY3, int):
                        #    kernel3 = np.ones((self.KerX3, self.KerY3), np.uint8)
                        #mascara3 = cv2.morphologyEx(mascara3, cv2.MORPH_CLOSE, kernel3)
                        #mascara3 = cv2.morphologyEx(mascara3, cv2.MORPH_OPEN, kernel3)
                        contorno3, _ = cv2.findContours(mascara3, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                        contour_image3 = np.zeros((frame.shape[0], frame.shape[1], 3), dtype=np.uint8)
                        if contorno3:
                            cv2.drawContours(contour_image3, contorno3, -1, (0, 255, 0), 2)
                            if contour_image3 is not None and contour_image3.shape[0] > 0 and contour_image3.shape[1] > 0:
                                qt_image_contour3 = QImage(contour_image3.data, contour_image3.shape[1], contour_image3.shape[0], contour_image3.strides[0], QImage.Format.Format_RGB888)
                                self.processed_frame_signal2.emit(qt_image_contour3)

                        #Color4-------------------------------------------
                        hsv4 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                        color_oscuro4 = np.array([self.TonMin4, self.PurMin4, self.LumMin4])
                        color_claro4 = np.array([self.TonMax4, self.PurMax4, self.LumMax4])
                        mascara4 = cv2.inRange(hsv4, color_oscuro4, color_claro4)
                        #if isinstance(self.KerX4, int) and isinstance(self.KerY4, int):
                        #    kernel4 = np.ones((self.KerX4, self.KerY4), np.uint8)
                        #mascara4 = cv2.morphologyEx(mascara4, cv2.MORPH_CLOSE, kernel4)
                        #mascara4 = cv2.morphologyEx(mascara4, cv2.MORPH_OPEN, kernel4)
                        contorno4, _ = cv2.findContours(mascara4, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                        contour_image4 = np.zeros((frame.shape[0], frame.shape[1], 3), dtype=np.uint8)
                        if contorno4:
                            cv2.drawContours(contour_image4, contorno4, -1, (0, 255, 0), 2)
                            if contour_image4 is not None and contour_image4.shape[0] > 0 and contour_image4.shape[1] > 0:
                                qt_image_contour4 = QImage(contour_image4.data, contour_image4.shape[1], contour_image4.shape[0], contour_image4.strides[0], QImage.Format.Format_RGB888)
                                self.processed_frame_signal3.emit(qt_image_contour4)

                    
                    QThread.msleep(60)


    def actualizar_dic_IPT(self,diccionario):
        self.diccionario_del_IPT = diccionario

        self.TonMin1 = self.diccionario_del_IPT.get("Tonalidad Minima S1")
        self.TonMax1 = self.diccionario_del_IPT.get("Tonalidad Maxima S1")
        self.PurMin1 = self.diccionario_del_IPT.get("Pureza Minima S1")
        self.PurMax1 = self.diccionario_del_IPT.get("Pureza Maxima S1")
        self.LumMin1 = self.diccionario_del_IPT.get("Luminosidad Minima S1")
        self.LumMax1 = self.diccionario_del_IPT.get("Luminosidad Maxima S1")
        self.KerX1 = self.diccionario_del_IPT.get("Kernel X S1")
        self.KerY1 = self.diccionario_del_IPT.get("Kernel y S1")
        self.TonMin2 = self.diccionario_del_IPT.get("Tonalidad Minima S2")
        self.TonMax2 = self.diccionario_del_IPT.get("Tonalidad Maxima S2")
        self.PurMin2 = self.diccionario_del_IPT.get("Pureza Minima S2")
        self.PurMax2 = self.diccionario_del_IPT.get("Pureza Maxima S2")
        self.LumMin2 = self.diccionario_del_IPT.get("Luminosidad Minima S2")
        self.LumMax2 = self.diccionario_del_IPT.get("Luminosidad Maxima S2")
        self.KerX2 = self.diccionario_del_IPT.get("Kernel X S2")
        self.KerY2 = self.diccionario_del_IPT.get("Kernel y S2")
        self.TonMin3 = self.diccionario_del_IPT.get("Tonalidad Minima S3")
        self.TonMax3 = self.diccionario_del_IPT.get("Tonalidad Maxima S3")
        self.PurMin3 = self.diccionario_del_IPT.get("Pureza Minima S3")
        self.PurMax3 = self.diccionario_del_IPT.get("Pureza Maxima S3")
        self.LumMin3 = self.diccionario_del_IPT.get("Luminosidad Minima S3")
        self.LumMax3 = self.diccionario_del_IPT.get("Luminosidad Maxima S3")
        self.KerX3 = self.diccionario_del_IPT.get("Kernel X S3")
        self.KerY3 = self.diccionario_del_IPT.get("Kernel y S3")
        self.TonMin4 = self.diccionario_del_IPT.get("Tonalidad Minima S4")
        self.TonMax4 = self.diccionario_del_IPT.get("Tonalidad Maxima S4")
        self.PurMin4 = self.diccionario_del_IPT.get("Pureza Minima S4")
        self.PurMax4 = self.diccionario_del_IPT.get("Pureza Maxima S4")
        self.LumMin4 = self.diccionario_del_IPT.get("Luminosidad Minima S4")
        self.LumMax4 = self.diccionario_del_IPT.get("Luminosidad Maxima S4")
        self.KerX4 = self.diccionario_del_IPT.get("Kernel X S4")
        self.KerY4 = self.diccionario_del_IPT.get("Kernel y S4")



    def set_selected_preset(self, preset):
        self.current_preset = preset

    def stop(self):
        self.running = False
        self.wait()

    def pausar(self):
        self.pausar_signal.emit()

    def reanudar(self):
        self.reanudar_signal.emit()
class Creadordesliders(QThread):
    update_signal = pyqtSignal(str, int)

    def __init__(self, sliders):
        super().__init__()
        self.sliders = sliders

    def run(self):
        while True:
            for slider_name, slider in self.sliders.items():
                self.update_signal.emit(slider_name, slider.value())
                self.msleep(100)  # Ajusta el tiempo de espera según tus necesidades
class DICThread(QThread):
    actualizar_signal = pyqtSignal(str, int)
    enviar_signal = pyqtSignal(dict)
    def __init__(self):
        super().__init__()
        self.diccionario_datos = {'Tonalidad Minima S1': 10, 'Tonalidad Maxima S1': 20, 'Pureza Minima S1': 30,"Pureza Maxima S1": 40,"Luminosidad Minima S1":50,"Luminosidad Maxima S1":60,"Kernel X S1":70,"Kernel Y S1" :80,
                                  'Tonalidad Minima S2': 10, 'Tonalidad Maxima S2': 20, 'Pureza Minima S2': 30,"Pureza Maxima S2": 40,"Luminosidad Minima S2":50,"Luminosidad Maxima S2":60,"Kernel X S2":70,"Kernel Y S2" :80,
                                  'Tonalidad Minima S3': 10, 'Tonalidad Maxima S3': 20, 'Pureza Minima S3': 30,"Pureza Maxima S3": 40,"Luminosidad Minima S3":50,"Luminosidad Maxima S3":60,"Kernel X S3":70,"Kernel Y S3" :80,
                                  'Tonalidad Minima S4': 10, 'Tonalidad Maxima S4': 20, 'Pureza Minima S4': 30,"Pureza Maxima S4": 40,"Luminosidad Minima S4":50,"Luminosidad Maxima S4":60,"Kernel X S4":70,"Kernel Y S4" :80
                                  }
        
        
    def run(self):
        self.actualizar_signal.connect(self.manejar_actualizacion)
        

    def manejar_actualizacion(self, nombre, valor):
        #print(f"Nombre y valor almacenados en el hilo secundario - Nombre: {nombre}, Valor: {valor}")
        self.diccionario_datos[nombre] = valor
        self.enviar_signal.emit(self.diccionario_datos)

    

#############################################################################################

class Ventana_Principal(QMainWindow):
    def __init__(self):
        super().__init__()
        try:
            self.dic_thread = DICThread()
            self.video_thread = VideoStreamThread()
            self.inicializarUI()
            self.shared_frame_queue = Queue()  # Crear la cola compartida
            self.barra_de_estado = QStatusBar()
            self.setStatusBar(self.barra_de_estado)
        except Exception as e:
            print(f"Excepción en el hilo de ejecución: {e}")
            
#generacion de UI Principal-----------------------------------------
    def inicializarUI(self):
        self.setGeometry(100,100,1400,750)
        self.setWindowTitle("Interfaz_v4.2") 
        self.generate_main_window()
        self.created_actions()
        self.show()
#aqui se colocan todas las demas ventanas
    def generate_main_window(self):
        self.create_menu()
        self.create_dock_modificacion_de_datos()
        self.create_ventana_central()
        
        self.create_dock_2()
#aqui se colocan las partes de generacion de actions
    def created_actions(self):
        self.create_action_modificacion_de_datos()
        self.create_action_Mascaras()
#aqui empieza la logica de la intterfaz

    def create_menu(self):
        self.menuBar()
        menu_view = self.menuBar().addMenu("Menú")
        #menu_view.addAction(self.Modificacion_de_datos)
        #menu_view.addAction(self.Mascaras)
#Primer dock---------------------------------------------------
    

    def create_dock_modificacion_de_datos(self):
        self.dock1 = QDockWidget()
        self.dock1.setWindowTitle("Modificacion de datos")
        self.dock1.setAllowedAreas(
            Qt.DockWidgetArea.AllDockWidgetAreas
        )
        self.contenedor_de_widgets = QWidget()
        main_box_dock1 = QGridLayout()
        # text1 = QLabel("Distancias entre marcas")
        # text1.setFixedHeight(20)
        # text1.setStyleSheet("background-color: #dadada")
        # main_box_dock1.addWidget(text1, 1, 0,1,2)
        # #Ingreso de datos-----------------------------------------------------------------
        # main_box_dock1.addWidget(QLabel('Distancia Rojo,Amarillo(cm):'), 2, 0)
        # main_box_dock1.addWidget(QLineEdit(), 2, 1)
        # main_box_dock1.addWidget(QLabel('Distancia Rojo,Azul(cm):'), 3, 0)
        # main_box_dock1.addWidget(QLineEdit(echoMode=QLineEdit.EchoMode.Password), 3, 1)
        # main_box_dock1.addWidget(QPushButton('Modificar'), 4, 0,1,2)
        
        #Filtro RGB---------------------------------------------------------------
        text2 = QLabel("Filtro RGB")
        text2.setFixedHeight(20)
        text2.setStyleSheet("background-color: #dadada")
        main_box_dock1.addWidget(text2, 6, 0,1,2)

        self.Widgget_contenedor_de_sliders = QWidget()
        self.tab_widget = QTabWidget(self.Widgget_contenedor_de_sliders)
        

        # Crear pestañas con contenido diferente
        tab1 = QWidget()
        self.sliders_tab1 = self.create_elements(tab1, [
            {"type": "slider", "name": "Tonalidad Minima S1", "min": 0, "max": 100, "initial_value": 50, "tick_interval": 10},
            {"type": "slider", "name": "Tonalidad Maxima S1", "min": 0, "max": 200, "initial_value": 100, "tick_interval": 20},
            {"type": "slider", "name": "Pureza Minima S1", "min": 0, "max": 50, "initial_value": 25, "tick_interval": 5},
            {"type": "slider", "name": "Pureza Maxima S1", "min": 0, "max": 50, "initial_value": 25, "tick_interval": 5},
            {"type": "slider", "name": "Luminosidad Minima S1", "min": 0, "max": 100, "initial_value": 50, "tick_interval": 10},
            {"type": "slider", "name": "Luminosidad Maxima S1", "min": 0, "max": 200, "initial_value": 100, "tick_interval": 20},
            {"type": "slider", "name": "Kernel X S1", "min": 0, "max": 2, "initial_value": 1, "tick_interval": 1},
            {"type": "slider", "name": "Kernel Y S1", "min": 0, "max": 2, "initial_value": 1, "tick_interval": 1}
        ])

        tab2 = QWidget()
        self.sliders_tab2 = self.create_elements(tab2, [
            {"type": "slider", "name": "Tonalidad Minima S2", "min": 0, "max": 100, "initial_value": 50, "tick_interval": 10},
            {"type": "slider", "name": "Tonalidad Maxima S2", "min": 0, "max": 200, "initial_value": 100, "tick_interval": 20},
            {"type": "slider", "name": "Pureza Minima S2", "min": 0, "max": 50, "initial_value": 25, "tick_interval": 5},
            {"type": "slider", "name": "Pureza Maxima S2", "min": 0, "max": 50, "initial_value": 25, "tick_interval": 5},
            {"type": "slider", "name": "Luminosidad Minima S2", "min": 0, "max": 100, "initial_value": 50, "tick_interval": 10},
            {"type": "slider", "name": "Luminosidad Maxima S2", "min": 0, "max": 200, "initial_value": 100, "tick_interval": 20},
            {"type": "slider", "name": "Kernel X S2", "min": 0, "max": 2, "initial_value": 1, "tick_interval": 1},
            {"type": "slider", "name": "Kernel Y S2", "min": 0, "max": 2, "initial_value": 1, "tick_interval": 1}
        ])
        tab3 = QWidget()
        self.sliders_tab3 = self.create_elements(tab3, [
            {"type": "slider", "name": "Tonalidad Minima S3", "min": 0, "max": 100, "initial_value": 50, "tick_interval": 10},
            {"type": "slider", "name": "Tonalidad Maxima S3", "min": 0, "max": 200, "initial_value": 100, "tick_interval": 20},
            {"type": "slider", "name": "Pureza Minima S3", "min": 0, "max": 50, "initial_value": 25, "tick_interval": 5},
            {"type": "slider", "name": "Pureza Maxima S3", "min": 0, "max": 50, "initial_value": 25, "tick_interval": 5},
            {"type": "slider", "name": "Luminosidad Minima S3", "min": 0, "max": 100, "initial_value": 50, "tick_interval": 10},
            {"type": "slider", "name": "Luminosidad Maxima S3", "min": 0, "max": 200, "initial_value": 100, "tick_interval": 20},
            {"type": "slider", "name": "Kernel X S3","min": 0, "max": 2, "initial_value": 1, "tick_interval": 1},
            {"type": "slider", "name": "Kernel Y S3", "min": 0, "max": 2, "initial_value": 1, "tick_interval": 1}
        ])
        tab4 = QWidget()
        self.sliders_tab4 = self.create_elements(tab4, [
            {"type": "slider", "name": "Tonalidad Minima S4", "min": 0, "max": 100, "initial_value": 50, "tick_interval": 10},
            {"type": "slider", "name": "Tonalidad Maxima S4", "min": 0, "max": 200, "initial_value": 100, "tick_interval": 20},
            {"type": "slider", "name": "Pureza Minima S4", "min": 0, "max": 50, "initial_value": 25, "tick_interval": 5},
            {"type": "slider", "name": "Pureza Maxima S4", "min": 0, "max": 50, "initial_value": 25, "tick_interval": 5},
            {"type": "slider", "name": "Luminosidad Minima S4", "min": 0, "max": 100, "initial_value": 50, "tick_interval": 10},
            {"type": "slider", "name": "Luminosidad Maxima S4", "min": 0, "max": 200, "initial_value": 100, "tick_interval": 20},
            {"type": "slider", "name": "Kernel X S4", "min": 0, "max": 2, "initial_value": 1, "tick_interval": 1},
            {"type": "slider", "name": "Kernel Y S4", "min": 0, "max": 2, "initial_value": 1, "tick_interval": 1}
        ])
        self.tab_Datos = QTableWidget()
        self.tab_Datos.setColumnCount(2)
        self.tab_Datos.setHorizontalHeaderLabels(['Nombre', 'Valor'])
        self.tab_Datos.setMinimumWidth(250)
        self.dic_thread.actualizar_signal.connect(self.actualizar_tabla)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.tab_Datos)
        scroll_area.setMinimumWidth(250)
        scroll_area.setMaximumHeight(220)

        

        # Agregar las pestañas al QTabWidget
        
        self.tab_widget.addTab(tab1, "Tab 1")
        self.tab_widget.addTab(tab2, "Tab 2")
        self.tab_widget.addTab(tab3, "Tab 3")
        self.tab_widget.addTab(tab4, "Tab 4")
        

        self.worker_thread = Creadordesliders({**self.sliders_tab1, **self.sliders_tab2, **self.sliders_tab3})
        self.worker_thread.update_signal.connect(self.handle_slider_change)
        self.worker_thread.start()
        self.dic_thread.start()
        self.actualizar_tabla_con_preset()
        
        main_box_dock1.addWidget(self.Widgget_contenedor_de_sliders,7,0,1,2)
        

        main_box_dock1.addWidget(scroll_area,9,0,1,2)
        self.contenedor_de_widgets.setLayout(main_box_dock1)
        
        self.dock1.setWidget(self.contenedor_de_widgets)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea,self.dock1)
        

    def actualizar_tabla(self, nombre, valor):
        # Verificar si el nombre ya existe en el diccionario
        if nombre in self.dic_thread.diccionario_datos:
            # Si existe, buscar la fila correspondiente y actualizar el valor
            for row in range(self.tab_Datos.rowCount()):
                item = self.tab_Datos.item(row, 0)
                if item and item.text() == nombre:
                    self.tab_Datos.setItem(row, 1, QTableWidgetItem(str(valor)))
                    break
        else:
            # Si no existe, agregar una nueva fila
            row_position = self.tab_Datos.rowCount()
            self.tab_Datos.insertRow(row_position)
            self.tab_Datos.setItem(row_position, 0, QTableWidgetItem(nombre))
            self.tab_Datos.setItem(row_position, 1, QTableWidgetItem(str(valor)))

    def actualizar_tabla_con_preset(self):
        for nombre, valor in self.dic_thread.diccionario_datos.items():
            row_position = self.tab_Datos.rowCount()
            self.tab_Datos.insertRow(row_position)
            self.tab_Datos.setItem(row_position, 0, QTableWidgetItem(nombre))
            self.tab_Datos.setItem(row_position, 1, QTableWidgetItem(str(valor)))

    def create_elements(self, tab, elements):
        tab_layout = QVBoxLayout(tab)
        sliders = {}

        for element in elements:
            if element["type"] == "slider":
                s = element["name"]
                s = QSlider(Qt.Orientation.Horizontal)
                s.setObjectName(element["name"])  # Asignar el nombre del slider
                s.setMinimum(element["min"])
                s.setMaximum(element["max"])
                s.setValue(element["initial_value"])
                #s.setTickInterval(element["tick_interval"])
                #s.setTickPosition(QSlider.TickPosition.TicksBelow)

                label = QLabel(element["name"])
                slider_last_value = [s.value()]

                def slider_changed(value, label=label, slider_name=element["name"], last_value=slider_last_value):
                    if value != last_value[0]:
                        self.handle_slider_change(slider_name, value)
                        last_value[0] = value
                        
                s.valueChanged.connect(slider_changed)
                tab_layout.addWidget(label)
                tab_layout.addWidget(s)
            
        return sliders

    def handle_slider_change(self, slider_name, value):
        #print(f"'{slider_name}' value changed:", value)
        self.dic_thread.actualizar_signal.emit(slider_name,value)
        #print("Si_se_envio_señal")
        



        
    

        

    def create_ventana_central(self):
        tab_bar = QTabWidget(self)
        self.contenedor1 = QWidget()
        
        ventana_video_principal = MiVentana(self.video_thread)
        tab_bar.addTab(ventana_video_principal,"contenedor1")
        self.contenedor2 = QWidget()
        tab_bar.addTab(self.contenedor2,"contenedor2")
        main_container = QWidget()


        tab_h_box = QHBoxLayout()
        tab_h_box.addWidget(tab_bar)
        main_container.setLayout(tab_h_box)
        self.setCentralWidget(main_container)
    
        
 
    def create_dock_2(self):
        midockwidget = MiDockWidget(self.video_thread,self.dic_thread)
        self.dock2 = QDockWidget()
        self.dock2.setWidget(midockwidget)

        self.dock2.setWindowTitle("Mascara y Resultados")
        self.dock2.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock2)


       


    def create_action_modificacion_de_datos(self):
        self.Modificacion_de_datos = QAction('Modificacion de datos',self,checkable=True)
        self.Modificacion_de_datos.setShortcut(QKeySequence("ctrl+L"))
        self.Modificacion_de_datos.setStatusTip("Aqui se pueden modificar los parametros generales del progama")
        self.Modificacion_de_datos.triggered.connect(self.Modificar_datosB)

    def create_action_Mascaras(self):
        self.Mascaras = QAction('Mascaras',self,checkable=True)
        self.Mascaras.setShortcut(QKeySequence("ctrl+I"))
        self.Mascaras.setStatusTip("Aqui se puede visualizar las mascaras")
        self.Mascaras.triggered.connect(self.Mascara)  
    def Modificar_datosB(self):
        if self.Modificacion_de_datos.isChecked():
            pass
        else:
            pass

    def Mascara(self):
        if self.Mascaras.isChecked():
            pass
        else:
            pass

    
    ###Aqui termina la parte de la interfaz
    
    ###Primer intento añadir video
    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = Ventana_Principal()
    sys.exit(app.exec())
