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
                            QScrollArea)
from PyQt6.QtGui import QImage, QPixmap,QAction,QKeySequence
from PyQt6.QtCore import Qt,QThread, pyqtSignal, QMutex, QMutexLocker,QTimer
import cv2
from queue import Queue
import numpy as np



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
                    print(f"Error al capturar el fotograma: {video_stream.get(cv2.CAP_PROP_FRAME_WIDTH)} x {video_stream.get(cv2.CAP_PROP_FRAME_HEIGHT)}")
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
        self.presets_combobox = QComboBox(self)
        self.presets_combobox.addItems(["Original", "Seleccion de colores", "Contornos"])

        # Crear instancia de ImageProcessorThread y pasarla a MiDockWidget
        self.image_processor_thread = ImageProcessorThread(self.hilo_video.get_latest_frame, self)
        
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
        self.margin_slider.valueChanged.connect(self.actualizar_margin)

        layout_principalQD.addWidget(self.margin_slider, 3, 1, 1, 2)

    def actualizar_margin(self, value):
        self.margin = value
        self.update_frame2(self.latest_image2)
        self.update_frame3(self.latest_image3)
        self.update_frame4(self.latest_image4)
        self.update_frame5(self.latest_image5)

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

    def update_frame5(self, image5):
        self.latest_image5 = image5
        margin = self.margin_slider.value()
        pixmap5 = QPixmap.fromImage(image5)
        pixmap5 = pixmap5.scaled(margin, margin, Qt.AspectRatioMode.KeepAspectRatio)
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

    def __init__(self, get_frame_function, mi_dock_widget):
        super().__init__()
        self.running = True
        self.paused = False
        self.get_frame_function = get_frame_function
        self.mi_dock_widget = mi_dock_widget

        self.presets_combobox = mi_dock_widget.presets_combobox

        # Conectar el evento currentIndexChanged al método update_preset de ImageProcessorThread
        self.presets_combobox.currentIndexChanged.connect(self.update_preset)

        # Inicializar el preset actual
        self.current_preset = 0

    def update_preset(self, index):
        self.current_preset = index
        self.mi_dock_widget.presets_combobox.setCurrentIndex(index)
##########################################################################aqui se conectan los sliders

    def run(self):
        while self.running:
            frame = self.get_frame_function()
            if frame is not None and frame.size != 0:
                if not self.paused:
                    if self.current_preset == 0:
                        qt_image_1 = QImage(frame.data, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format.Format_RGB888)
                        self.processed_frame_signal.emit(qt_image_1)

                        
                    
                    elif self.current_preset == 1:
                        qt_image_2 = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
                        qt_image_2 = QImage(qt_image_2.data, qt_image_2.shape[1], qt_image_2.shape[0], qt_image_2.strides[0], QImage.Format.Format_RGB888)
                        self.processed_frame_signal1.emit(qt_image_2)
                        
                        qt_image_2 = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
                        qt_image_2 = QImage(qt_image_2.data, qt_image_2.shape[1], qt_image_2.shape[0], qt_image_2.strides[0], QImage.Format.Format_RGB888)
                        self.processed_frame_signal1.emit(qt_image_2)

                        qt_image_2 = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
                        qt_image_2 = QImage(qt_image_2.data, qt_image_2.shape[1], qt_image_2.shape[0], qt_image_2.strides[0], QImage.Format.Format_RGB888)
                        self.processed_frame_signal1.emit(qt_image_2)

                        qt_image_2 = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
                        qt_image_2 = QImage(qt_image_2.data, qt_image_2.shape[1], qt_image_2.shape[0], qt_image_2.strides[0], QImage.Format.Format_RGB888)
                        self.processed_frame_signal1.emit(qt_image_2)
                    elif self.current_preset == 2:
                        qt_image_1 = QImage(frame.data, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format.Format_RGB888)
                        self.processed_frame_signal.emit(qt_image_1)

                        
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

#############################################################################################

class Ventana_Principal(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.video_thread = VideoStreamThread()
        self.inicializarUI()
        self.shared_frame_queue = Queue()  # Crear la cola compartida
        self.barra_de_estado = QStatusBar()
        self.setStatusBar(self.barra_de_estado)
#generacion de UI Principal-----------------------------------------
    def inicializarUI(self):
        self.setGeometry(100,100,1400,750)
        self.setWindowTitle("Interfaz_v2.4") 
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
        text2 = QLabel("Distancias entre marcas")
        text2.setStyleSheet("background-color: #dadada")
        main_box_dock1.addWidget(text2, 1, 0,1,2)
        #Ingreso de datos-----------------------------------------------------------------
        main_box_dock1.addWidget(QLabel('Distancia Rojo,Amarillo(cm):'), 2, 0)
        main_box_dock1.addWidget(QLineEdit(), 2, 1)
        main_box_dock1.addWidget(QLabel('Distancia Rojo,Azul(cm):'), 3, 0)
        main_box_dock1.addWidget(QLineEdit(echoMode=QLineEdit.EchoMode.Password), 3, 1)
        main_box_dock1.addWidget(QPushButton('Modificar'), 4, 0,1,2)
        
        #Filtro RGB---------------------------------------------------------------
        text2 = QLabel("Filtro RGB")
        text2.setStyleSheet("background-color: #dadada")
        main_box_dock1.addWidget(text2, 6, 0,1,2)

        contenedor_de_Filtro_RGB_layout = QGridLayout()
        contenedor_de_Filtro_RGB = QWidget()
        tab_bar_filtro_RGB = QTabWidget()
        #Filtro1------------------------------------------------------------
        self.Filtro1 = QWidget()
        contenedor_filtro1 = QVBoxLayout()
        text_sl1_2 = QLabel("Tonalidad")
        contenedor_filtro1.addWidget(text_sl1_2)
        slider1 = QSlider(Qt.Orientation.Horizontal,self)
        slider1.setRange(0, 255)
        slider1.setValue(50)
        slider1.setSingleStep(5) 
        slider1.valueChanged.connect(self.Valorsl1)
        self.textvaluesl1 = QLabel('', self)
        
        contenedor_filtro1.addWidget(slider1)
        contenedor_filtro1.addWidget(self.textvaluesl1)
 
        slider2 = QSlider(Qt.Orientation.Horizontal,self)
        slider2.setRange(0, 255)
        slider2.setValue(50)
        slider2.setSingleStep(5) 
        slider2.valueChanged.connect(self.Valorsl2)
        self.textvaluesl2 = QLabel('', self)
        contenedor_filtro1.addWidget(slider2)
        contenedor_filtro1.addWidget(self.textvaluesl2)

        text_sl3_4 = QLabel("pureza")
        contenedor_filtro1.addWidget(text_sl3_4)
        slider3 = QSlider(Qt.Orientation.Horizontal,self)
        slider3.setRange(0, 255)
        slider3.setValue(50)
        slider3.setSingleStep(5) 
        slider3.valueChanged.connect(self.Valorsl3)
        self.textvaluesl3 = QLabel('', self)
        contenedor_filtro1.addWidget(slider3)
        contenedor_filtro1.addWidget(self.textvaluesl3)

        contenedor_filtro1.addWidget(slider3)
        slider4 = QSlider(Qt.Orientation.Horizontal,self) 
        slider4.setRange(0, 255)
        slider4.setValue(50)
        slider4.setSingleStep(5) 
        slider4.valueChanged.connect(self.Valorsl4)
        self.textvaluesl4 = QLabel('', self)
        contenedor_filtro1.addWidget(slider4)
        contenedor_filtro1.addWidget(self.textvaluesl4)
        text_sl5_6 = QLabel("Luminosidad")
        contenedor_filtro1.addWidget(text_sl5_6)
        slider5 = QSlider(Qt.Orientation.Horizontal,self)
        slider5.setRange(0, 255)
        slider5.setValue(50)
        slider5.setSingleStep(5) 
        slider5.valueChanged.connect(self.Valorsl5)
        self.textvaluesl5 = QLabel('', self)
        contenedor_filtro1.addWidget(slider5)
        contenedor_filtro1.addWidget(self.textvaluesl5)
        
        slider6 = QSlider(Qt.Orientation.Horizontal,self)
        slider6.setRange(0, 255)
        slider6.setValue(50)
        slider6.setSingleStep(5) 
        slider6.valueChanged.connect(self.Valorsl6)
        self.textvaluesl6 = QLabel('', self)
        contenedor_filtro1.addWidget(slider6)
        
        contenedor_filtro1.addWidget(self.textvaluesl6)
        
        text_sl7_8 = QLabel("Kernel")
        contenedor_filtro1.addWidget(text_sl7_8)
        slider7 = QSlider(Qt.Orientation.Horizontal,self)
        slider7.setRange(0, 15)
        slider7.setValue(1)
        slider7.setSingleStep(1) 
        slider7.valueChanged.connect(self.Valorsl7)
        self.textvaluesl7 = QLabel('', self)
        contenedor_filtro1.addWidget(slider7)
        contenedor_filtro1.addWidget(self.textvaluesl7)
        slider8 = QSlider(Qt.Orientation.Horizontal,self)
        slider8.setRange(0, 12)
        slider8.setValue(1)
        slider8.setSingleStep(1) 
        slider8.valueChanged.connect(self.Valorsl8)
        self.textvaluesl8 = QLabel('', self)
        contenedor_filtro1.addWidget(slider8)
        contenedor_filtro1.addWidget(self.textvaluesl8)

        self.Filtro1.setLayout(contenedor_filtro1)
        #filtro2---------------------------------------------------------------
        self.Filtro2 = QWidget()
        contenedor_filtro2 = QVBoxLayout()
        text_sl1_22 = QLabel("Tonalidad")
        contenedor_filtro2.addWidget(text_sl1_22)
        slider9 = QSlider(Qt.Orientation.Horizontal,self)
        slider9.setRange(0, 255)
        slider9.setValue(50)
        slider9.setSingleStep(5) 
        slider9.valueChanged.connect(self.Valorsl9)
        self.textvaluesl9 = QLabel('', self)
        
        contenedor_filtro2.addWidget(slider9)
        contenedor_filtro2.addWidget(self.textvaluesl9)
 
        slider10 = QSlider(Qt.Orientation.Horizontal,self)
        slider10.setRange(0, 255)
        slider10.setValue(50)
        slider10.setSingleStep(5) 
        slider10.valueChanged.connect(self.Valorsl10)
        self.textvaluesl10 = QLabel('', self)
        contenedor_filtro2.addWidget(slider10)
        contenedor_filtro2.addWidget(self.textvaluesl10)

        text_sl3_42 = QLabel("pureza")
        contenedor_filtro2.addWidget(text_sl3_42)
        slider11 = QSlider(Qt.Orientation.Horizontal,self)
        slider11.setRange(0, 255)
        slider11.setValue(50)
        slider11.setSingleStep(5) 
        slider11.valueChanged.connect(self.Valorsl11)
        self.textvaluesl11 = QLabel('', self)
        contenedor_filtro2.addWidget(slider11)
        contenedor_filtro2.addWidget(self.textvaluesl11)

        slider12 = QSlider(Qt.Orientation.Horizontal,self) 
        slider12.setRange(0, 255)
        slider12.setValue(50)
        slider12.setSingleStep(5) 
        slider12.valueChanged.connect(self.Valorsl12)
        self.textvaluesl12 = QLabel('', self)
        contenedor_filtro2.addWidget(slider12)
        contenedor_filtro2.addWidget(self.textvaluesl12)

        text_sl5_62 = QLabel("Luminosidad")
        contenedor_filtro2.addWidget(text_sl5_62)
        slider13 = QSlider(Qt.Orientation.Horizontal,self)
        slider13.setRange(0, 255)
        slider13.setValue(50)
        slider13.setSingleStep(5) 
        slider13.valueChanged.connect(self.Valorsl13)
        self.textvaluesl13 = QLabel('', self)
        contenedor_filtro2.addWidget(slider13)
        contenedor_filtro2.addWidget(self.textvaluesl13)
        
        slider14 = QSlider(Qt.Orientation.Horizontal,self)
        slider14.setRange(0, 255)
        slider14.setValue(50)
        slider14.setSingleStep(5) 
        slider14.valueChanged.connect(self.Valorsl14)
        self.textvaluesl14 = QLabel('', self)
        
        contenedor_filtro2.addWidget(slider14)
        contenedor_filtro2.addWidget(self.textvaluesl14)
        
    
        text_sl7_82 = QLabel("Kernel")
        contenedor_filtro2.addWidget(text_sl7_82)
        slider15 = QSlider(Qt.Orientation.Horizontal,self)
        slider15.setRange(0, 15)
        slider15.setValue(1)
        slider15.setSingleStep(1) 
        slider15.valueChanged.connect(self.Valorsl15)
        self.textvaluesl15 = QLabel('', self)
        contenedor_filtro2.addWidget(slider15)
        contenedor_filtro2.addWidget(self.textvaluesl15)
        
        slider16 = QSlider(Qt.Orientation.Horizontal,self)
        slider16.setRange(0, 12)
        slider16.setValue(1)
        slider16.setSingleStep(1) 
        slider16.valueChanged.connect(self.Valorsl16)
        self.textvaluesl16 = QLabel('', self)
        contenedor_filtro2.addWidget(slider16)
        contenedor_filtro2.addWidget(self.textvaluesl16)

        #filtro3---------------------------------------------------------------
        self.Filtro3 = QWidget()
        contenedor_filtro3 = QVBoxLayout()
        text_sl1_23 = QLabel("Tonalidad")
        contenedor_filtro3.addWidget(text_sl1_23)
        slider17 = QSlider(Qt.Orientation.Horizontal,self)
        slider17.setRange(0, 255)
        slider17.setValue(50)
        slider17.setSingleStep(5) 
        slider17.valueChanged.connect(self.Valorsl17)
        self.textvaluesl17 = QLabel('', self)
        
        contenedor_filtro3.addWidget(slider17)
        contenedor_filtro3.addWidget(self.textvaluesl17)
 
        slider18 = QSlider(Qt.Orientation.Horizontal,self)
        slider18.setRange(0, 255)
        slider18.setValue(50)
        slider18.setSingleStep(5) 
        slider18.valueChanged.connect(self.Valorsl18)
        self.textvaluesl18 = QLabel('', self)
        contenedor_filtro3.addWidget(slider18)
        contenedor_filtro3.addWidget(self.textvaluesl18)

        text_sl3_43 = QLabel("pureza")
        contenedor_filtro3.addWidget(text_sl3_43)
        slider19 = QSlider(Qt.Orientation.Horizontal,self)
        slider19.setRange(0, 255)
        slider19.setValue(50)
        slider19.setSingleStep(5) 
        slider19.valueChanged.connect(self.Valorsl19)
        self.textvaluesl19 = QLabel('', self)
        contenedor_filtro3.addWidget(slider19)
        contenedor_filtro3.addWidget(self.textvaluesl19)
        

        slider20 = QSlider(Qt.Orientation.Horizontal,self) 
        slider20.setRange(0, 255)
        slider20.setValue(50)
        slider20.setSingleStep(5) 
        slider20.valueChanged.connect(self.Valorsl20)
        self.textvaluesl20 = QLabel('', self)
        contenedor_filtro3.addWidget(slider20)
        contenedor_filtro3.addWidget(self.textvaluesl20)

        text_sl5_62 = QLabel("Luminosidad")
        contenedor_filtro3.addWidget(text_sl5_62)
        slider21 = QSlider(Qt.Orientation.Horizontal,self)
        slider21.setRange(0, 255)
        slider21.setValue(50)
        slider21.setSingleStep(5) 
        slider21.valueChanged.connect(self.Valorsl21)
        self.textvaluesl21 = QLabel('', self)
        contenedor_filtro3.addWidget(slider21)
        contenedor_filtro3.addWidget(self.textvaluesl21)
        
        slider22 = QSlider(Qt.Orientation.Horizontal,self)
        slider22.setRange(0, 255)
        slider22.setValue(50)
        slider22.setSingleStep(5) 
        slider22.valueChanged.connect(self.Valorsl22)
        self.textvaluesl22 = QLabel('', self)
        
        contenedor_filtro3.addWidget(slider22)
        contenedor_filtro3.addWidget(self.textvaluesl22)
        
    
        text_sl7_82 = QLabel("Kernel")
        contenedor_filtro3.addWidget(text_sl7_82)
        slider23 = QSlider(Qt.Orientation.Horizontal,self)
        slider23.setRange(0, 15)
        slider23.setValue(1)
        slider23.setSingleStep(1) 
        slider23.valueChanged.connect(self.Valorsl23)
        self.textvaluesl23 = QLabel('', self)
        contenedor_filtro3.addWidget(slider23)
        contenedor_filtro3.addWidget(self.textvaluesl23)
        
        slider24 = QSlider(Qt.Orientation.Horizontal,self)
        slider24.setRange(0, 12)
        slider24.setValue(1)
        slider24.setSingleStep(1) 
        slider24.valueChanged.connect(self.Valorsl24)
        self.textvaluesl24 = QLabel('', self)
        contenedor_filtro3.addWidget(slider24)
        contenedor_filtro3.addWidget(self.textvaluesl24)

        #filtro4---------------------------------------------------------------
        self.Filtro4 = QWidget()
        contenedor_filtro4 = QVBoxLayout()
        text_sl1_24 = QLabel("Tonalidad")
        contenedor_filtro4.addWidget(text_sl1_24)
        slider25 = QSlider(Qt.Orientation.Horizontal,self)
        slider25.setRange(0, 255)
        slider25.setValue(50)
        slider25.setSingleStep(5) 
        slider25.valueChanged.connect(self.Valorsl25)
        self.textvaluesl25 = QLabel('', self)
        
        contenedor_filtro4.addWidget(slider25)
        contenedor_filtro4.addWidget(self.textvaluesl25)
 
        slider26 = QSlider(Qt.Orientation.Horizontal,self)
        slider26.setRange(0, 255)
        slider26.setValue(50)
        slider26.setSingleStep(5) 
        slider26.valueChanged.connect(self.Valorsl26)
        self.textvaluesl26 = QLabel('', self)
        contenedor_filtro4.addWidget(slider26)
        contenedor_filtro4.addWidget(self.textvaluesl26)

        text_sl3_44 = QLabel("pureza")
        contenedor_filtro4.addWidget(text_sl3_44)
        slider27 = QSlider(Qt.Orientation.Horizontal,self)
        slider27.setRange(0, 255)
        slider27.setValue(50)
        slider27.setSingleStep(5) 
        slider27.valueChanged.connect(self.Valors27)
        self.textvaluesl27 = QLabel('', self)
        contenedor_filtro4.addWidget(slider27)
        contenedor_filtro4.addWidget(self.textvaluesl27)
    

        slider28 = QSlider(Qt.Orientation.Horizontal,self) 
        slider28.setRange(0, 255)
        slider28.setValue(50)
        slider28.setSingleStep(5) 
        slider28.valueChanged.connect(self.Valorsl28)
        self.textvaluesl28 = QLabel('', self)
        contenedor_filtro4.addWidget(slider28)
        contenedor_filtro4.addWidget(self.textvaluesl28)

        text_sl5_64 = QLabel("Luminosidad")
        contenedor_filtro4.addWidget(text_sl5_64)
        slider29 = QSlider(Qt.Orientation.Horizontal,self)
        slider29.setRange(0, 255)
        slider29.setValue(50)
        slider29.setSingleStep(5) 
        slider29.valueChanged.connect(self.Valorsl29)
        self.textvaluesl29 = QLabel('', self)
        contenedor_filtro4.addWidget(slider29)
        contenedor_filtro4.addWidget(self.textvaluesl29)
        
        slider30 = QSlider(Qt.Orientation.Horizontal,self)
        slider30.setRange(0, 255)
        slider30.setValue(50)
        slider30.setSingleStep(5) 
        slider30.valueChanged.connect(self.Valorsl30)
        self.textvaluesl30 = QLabel('', self)
        
        contenedor_filtro4.addWidget(slider30)
        contenedor_filtro4.addWidget(self.textvaluesl30)
        
    
        text_sl7_84 = QLabel("Kernel")
        contenedor_filtro4.addWidget(text_sl7_84)
        slider31 = QSlider(Qt.Orientation.Horizontal,self)
        slider31.setRange(0, 15)
        slider31.setValue(1)
        slider31.setSingleStep(1) 
        slider31.valueChanged.connect(self.Valorsl31)
        self.textvaluesl31= QLabel('', self)
        contenedor_filtro4.addWidget(slider31)
        contenedor_filtro4.addWidget(self.textvaluesl31)
        
        slider32 = QSlider(Qt.Orientation.Horizontal,self)
        slider32.setRange(0, 12)
        slider32.setValue(1)
        slider32.setSingleStep(1) 
        slider32.valueChanged.connect(self.Valorsl32)
        self.textvaluesl32 = QLabel('', self)
        contenedor_filtro4.addWidget(slider32)
        contenedor_filtro4.addWidget(self.textvaluesl32)

       


        contenedor_filtro1.setSpacing(0)
        self.Filtro1.setLayout(contenedor_filtro1)

        contenedor_filtro2.setSpacing(0)
        self.Filtro2.setLayout(contenedor_filtro2)

        contenedor_filtro3.setSpacing(0)
        self.Filtro3.setLayout(contenedor_filtro3)

        contenedor_filtro4.setSpacing(0)
        self.Filtro4.setLayout(contenedor_filtro4)
        





        tab_bar_filtro_RGB.addTab(self.Filtro1,"Filtro color 1")
        tab_bar_filtro_RGB.addTab(self.Filtro2,"Filtro color 2")
        tab_bar_filtro_RGB.addTab(self.Filtro3,"Filtro color 3")
        tab_bar_filtro_RGB.addTab(self.Filtro4,"Filtro color 4")

        contenedor_de_Filtro_RGB_layout.addWidget(tab_bar_filtro_RGB)
        contenedor_de_Filtro_RGB.setLayout(contenedor_de_Filtro_RGB_layout)


        main_box_dock1.addWidget(contenedor_de_Filtro_RGB,7,0,1,2)
        main_box_dock1.setRowStretch(8,1)

        self.contenedor_de_widgets.setLayout(main_box_dock1)
        self.dock1.setWidget(self.contenedor_de_widgets)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea,self.dock1)
        

    

        

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
        midockwidget = MiDockWidget(self.video_thread)
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

    def Valorsl1(self,value):
        self.textvaluesl1.setText(f'Tonalidad minima: {value}')
        self.textvaluesl1.setStyleSheet('''
                border: 2px solid;
                border-radius: 8px;
                ''')
    def Valorsl2(self,value):
        self.textvaluesl2.setText(f'Tonalidad maxima: {value}')
        self.textvaluesl2.setStyleSheet('''
                border: 2px solid;
                border-radius: 8px;
                ''')
    def Valorsl3(self,value):
        self.textvaluesl3.setText(f'pureza minima: {value}')
        self.textvaluesl3.setStyleSheet('''
                border: 2px solid;
                border-radius: 8px;
                ''')
    def Valorsl4(self,value):
        self.textvaluesl4.setText(f'pureza maxima: {value}')
        self.textvaluesl4.setStyleSheet('''
                border: 2px solid;
                border-radius: 8px;
                ''')
    def Valorsl5(self,value):
        self.textvaluesl5.setText(f'luminosidad minima: {value}')
        self.textvaluesl5.setStyleSheet('''
                border: 2px solid;
                border-radius: 8px;
                ''')
    def Valorsl6(self,value):
        self.textvaluesl6.setText(f'luminosidad maxima: {value}')
        self.textvaluesl6.setStyleSheet('''
                border: 2px solid;
                border-radius: 8px;
                ''')
    def Valorsl7(self,value):
        self.textvaluesl7.setText(f'kernel minimo: {value}')
        self.textvaluesl7.setStyleSheet('''
                border: 2px solid;
                border-radius: 8px;
                ''')
    def Valorsl8(self,value):
        self.textvaluesl8.setText(f'kernel maximo: {value}')
        self.textvaluesl8.setStyleSheet('''
                border: 2px solid;
                border-radius: 8px;
                ''')
    def Valorsl9(self,value):
        self.textvaluesl9.setText(f'Tonalidad minima: {value}')
        self.textvaluesl9.setStyleSheet('''
                border: 2px solid;
                border-radius: 8px;
                ''')
    def Valorsl10(self,value):
        self.textvaluesl10.setText(f'Tonalidad maxima: {value}')
        self.textvaluesl10.setStyleSheet('''
                border: 2px solid;
                border-radius: 8px;
                ''')
    def Valorsl11(self,value):
        self.textvaluesl11.setText(f'pureza minima: {value}')
        self.textvaluesl11.setStyleSheet('''
                border: 2px solid;
                border-radius: 8px;
                ''')
    def Valorsl12(self,value):
        self.textvaluesl12.setText(f'pureza maxima: {value}')
        self.textvaluesl12.setStyleSheet('''
                border: 2px solid;
                border-radius: 8px;
                ''')
    def Valorsl13(self,value):
        self.textvaluesl13.setText(f'luminosidad minima: {value}')
        self.textvaluesl13.setStyleSheet('''
                border: 2px solid;
                border-radius: 8px;
                ''')
    def Valorsl14(self,value):
        self.textvaluesl14.setText(f'luminosidad maxima: {value}')
        self.textvaluesl14.setStyleSheet('''
                border: 2px solid;
                border-radius: 8px;
                ''')
    def Valorsl15(self,value):
        self.textvaluesl15.setText(f'kernel minimo: {value}')
        self.textvaluesl15.setStyleSheet('''
                border: 2px solid;
                border-radius: 8px;
                ''')
    def Valorsl16(self,value):
        self.textvaluesl16.setText(f'kernel maximo: {value}')
        self.textvaluesl16.setStyleSheet('''
                border: 2px solid;
                border-radius: 8px;
                ''')
    def Valorsl17(self,value):
        self.textvaluesl17.setText(f'Tonalidad minima: {value}')
        self.textvaluesl17.setStyleSheet('''
                border: 2px solid;
                border-radius: 8px;
                ''')
    def Valorsl18(self,value):
        self.textvaluesl18.setText(f'Tonalidad maxima: {value}')
        self.textvaluesl18.setStyleSheet('''
                border: 2px solid;
                border-radius: 8px;
                ''')
    def Valorsl19(self,value):
        self.textvaluesl19.setText(f'pureza minima: {value}')
        self.textvaluesl19.setStyleSheet('''
                border: 2px solid;
                border-radius: 8px;
                ''')
    def Valorsl20(self,value):
        self.textvaluesl20.setText(f'pureza maxima: {value}')
        self.textvaluesl20.setStyleSheet('''
                border: 2px solid;
                border-radius: 8px;
                ''')
    def Valorsl21(self,value):
        self.textvaluesl21.setText(f'luminosidad minima: {value}')
        self.textvaluesl21.setStyleSheet('''
                border: 2px solid;
                border-radius: 8px;
                ''')
    def Valorsl22(self,value):
        self.textvaluesl22.setText(f'luminosidad maxima: {value}')
        self.textvaluesl22.setStyleSheet('''
                border: 2px solid;
                border-radius: 8px;
                ''')
    def Valorsl23(self,value):
        self.textvaluesl23.setText(f'kernel minimo: {value}')
        self.textvaluesl23.setStyleSheet('''
                border: 2px solid;
                border-radius: 8px;
                ''')
    def Valorsl24(self,value):
        self.textvaluesl24.setText(f'kernel maximo: {value}')
        self.textvaluesl24.setStyleSheet('''
                border: 2px solid;
                border-radius: 8px;
                ''')
    def Valorsl25(self,value):
        self.textvaluesl25.setText(f'Tonalidad minima: {value}')
        self.textvaluesl25.setStyleSheet('''
                border: 2px solid;
                border-radius: 8px;
                ''')
    def Valorsl26(self,value):
        self.textvaluesl26.setText(f'Tonalidad maxima: {value}')
        self.textvaluesl26.setStyleSheet('''
                border: 2px solid;
                border-radius: 8px;
                ''')
    def Valors27(self,value):
        self.textvaluesl27.setText(f'pureza minima: {value}')
        self.textvaluesl27.setStyleSheet('''
                border: 2px solid;
                border-radius: 8px;
                ''')
    def Valorsl28(self,value):
        self.textvaluesl28.setText(f'pureza maxima: {value}')
        self.textvaluesl28.setStyleSheet('''
                border: 2px solid;
                border-radius: 8px;
                ''')
    def Valorsl29(self,value):
        self.textvaluesl29.setText(f'luminosidad minima: {value}')
        self.textvaluesl29.setStyleSheet('''
                border: 2px solid;
                border-radius: 8px;
                ''')
    def Valorsl30(self,value):
        self.textvaluesl30.setText(f'luminosidad maxima: {value}')
        self.textvaluesl30.setStyleSheet('''
                border: 2px solid;
                border-radius: 8px;
                ''')
    def Valorsl31(self,value):
        self.textvaluesl31.setText(f'kernel minimo: {value}')
        self.textvaluesl31.setStyleSheet('''
                border: 2px solid;
                border-radius: 8px;
                ''')
    def Valorsl32(self,value):
        self.textvaluesl32.setText(f'kernel maximo: {value}')
        self.textvaluesl32.setStyleSheet('''
                border: 2px solid;
                border-radius: 8px;
                ''')

    
    

    ###Aqui termina la parte de la interfaz
    
    ###Primer intento añadir video
    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = Ventana_Principal()
    sys.exit(app.exec())
