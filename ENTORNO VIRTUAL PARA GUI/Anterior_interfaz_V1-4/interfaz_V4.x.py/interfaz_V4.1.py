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
            pixmap2 = pixmap2.scaled(self.margin_value, self.margin_value, Qt.AspectRatioMode.KeepAspectRatio)
            self.label2.setPixmap(pixmap2)

    def update_frame3(self, image3=None):
        if image3 is not None:
            pixmap3 = QPixmap.fromImage(image3)
            pixmap3 = pixmap3.scaled(self.margin_value, self.margin_value, Qt.AspectRatioMode.KeepAspectRatio)
            self.label3.setPixmap(pixmap3)

    def update_frame4(self, image4=None):
        if image4 is not None:
            pixmap4 = QPixmap.fromImage(image4)
            pixmap4 = pixmap4.scaled(self.margin_value, self.margin_value, Qt.AspectRatioMode.KeepAspectRatio)
            self.label4.setPixmap(pixmap4)

    def update_frame5(self, image5=None):
        if image5 is not None:
            pixmap5 = QPixmap.fromImage(image5)
            pixmap5 = pixmap5.scaled(self.margin_value, self.margin_value, Qt.AspectRatioMode.KeepAspectRatio)
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
                    TonMin1 = self.diccionario_del_IPT.get("Tonalidad Minima S1")
                    print(TonMin1)

                    if self.current_preset == "Original":
                        qt_image_1 = QImage(frame.data, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format.Format_RGB888)
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
                        qt_image_1 = QImage(frame.data, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format.Format_RGB888)
                        self.processed_frame_signal3.emit(qt_image_1)

                        qt_image_2 = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
                        qt_image_2 = QImage(qt_image_2.data, qt_image_2.shape[1], qt_image_2.shape[0], qt_image_2.strides[0], QImage.Format.Format_Grayscale8)
                        self.processed_frame_signal.emit(qt_image_2)

                        qt_image_3 = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
                        qt_image_3 = QImage(qt_image_3.data, qt_image_3.shape[1], qt_image_3.shape[0], qt_image_3.strides[0], QImage.Format.Format_Grayscale8)
                        self.processed_frame_signal2.emit(qt_image_3)
                        
                    
                        qt_image_4 = cv2.applyColorMap(frame, cv2.COLORMAP_JET)
                        qt_image_4 = QImage(qt_image_4.data, qt_image_4.shape[1], qt_image_4.shape[0], qt_image_4.strides[0], QImage.Format.Format_RGB888)
                        self.processed_frame_signal1.emit(qt_image_4)
                        
                        

                    elif self.current_preset == "Contornos":
                        qt_image_1 = QImage(frame.data, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format.Format_RGB888)
                        self.processed_frame_signal1.emit(qt_image_1)

                        qt_image_2 = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
                        qt_image_2 = QImage(qt_image_2.data, qt_image_2.shape[1], qt_image_2.shape[0], qt_image_2.strides[0], QImage.Format.Format_Grayscale8)
                        self.processed_frame_signal3.emit(qt_image_2)

                        qt_image_3 = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
                        qt_image_3 = QImage(qt_image_3.data, qt_image_3.shape[1], qt_image_3.shape[0], qt_image_3.strides[0], QImage.Format.Format_Grayscale8)
                        self.processed_frame_signal.emit(qt_image_3)
                        
                    
                        qt_image_4 = cv2.applyColorMap(frame, cv2.COLORMAP_JET)
                        qt_image_4 = QImage(qt_image_4.data, qt_image_4.shape[1], qt_image_4.shape[0], qt_image_4.strides[0], QImage.Format.Format_RGB888)
                        self.processed_frame_signal2.emit(qt_image_4)
                    
                    
                    QThread.msleep(60)
            else:
                pass
    def actualizar_dic_IPT(self,diccionario):
        self.diccionario_del_IPT = diccionario
        


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
        self.dic_thread = DICThread()
        self.video_thread = VideoStreamThread()
        self.inicializarUI()
        self.shared_frame_queue = Queue()  # Crear la cola compartida
        self.barra_de_estado = QStatusBar()
        self.setStatusBar(self.barra_de_estado)
#generacion de UI Principal-----------------------------------------
    def inicializarUI(self):
        self.setGeometry(100,100,1400,750)
        self.setWindowTitle("Interfaz_v4.1") 
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
            {"type": "slider", "name": "Kernel X S1", "min": 0, "max": 50, "initial_value": 25, "tick_interval": 5},
            {"type": "slider", "name": "Kernel Y S1", "min": 0, "max": 50, "initial_value": 25, "tick_interval": 5}
        ])

        tab2 = QWidget()
        self.sliders_tab2 = self.create_elements(tab2, [
            {"type": "slider", "name": "Tonalidad Minima S2", "min": 0, "max": 100, "initial_value": 50, "tick_interval": 10},
            {"type": "slider", "name": "Tonalidad Maxima S2", "min": 0, "max": 200, "initial_value": 100, "tick_interval": 20},
            {"type": "slider", "name": "Pureza Minima S2", "min": 0, "max": 50, "initial_value": 25, "tick_interval": 5},
            {"type": "slider", "name": "Pureza Maxima S2", "min": 0, "max": 50, "initial_value": 25, "tick_interval": 5},
            {"type": "slider", "name": "Luminosidad Minima S2", "min": 0, "max": 100, "initial_value": 50, "tick_interval": 10},
            {"type": "slider", "name": "Luminosidad Maxima S2", "min": 0, "max": 200, "initial_value": 100, "tick_interval": 20},
            {"type": "slider", "name": "Kernel X S2", "min": 0, "max": 50, "initial_value": 25, "tick_interval": 5},
            {"type": "slider", "name": "Kernel Y S2", "min": 0, "max": 50, "initial_value": 25, "tick_interval": 5}
        ])
        tab3 = QWidget()
        self.sliders_tab3 = self.create_elements(tab3, [
            {"type": "slider", "name": "Tonalidad Minima S3", "min": 0, "max": 100, "initial_value": 50, "tick_interval": 10},
            {"type": "slider", "name": "Tonalidad Maxima S3", "min": 0, "max": 200, "initial_value": 100, "tick_interval": 20},
            {"type": "slider", "name": "Pureza Minima S3", "min": 0, "max": 50, "initial_value": 25, "tick_interval": 5},
            {"type": "slider", "name": "Pureza Maxima S3", "min": 0, "max": 50, "initial_value": 25, "tick_interval": 5},
            {"type": "slider", "name": "Luminosidad Minima S3", "min": 0, "max": 100, "initial_value": 50, "tick_interval": 10},
            {"type": "slider", "name": "Luminosidad Maxima S3", "min": 0, "max": 200, "initial_value": 100, "tick_interval": 20},
            {"type": "slider", "name": "Kernel X S3", "min": 0, "max": 50, "initial_value": 25, "tick_interval": 5},
            {"type": "slider", "name": "Kernel Y S3", "min": 0, "max": 50, "initial_value": 25, "tick_interval": 5}
        ])
        tab4 = QWidget()
        self.sliders_tab4 = self.create_elements(tab4, [
            {"type": "slider", "name": "Tonalidad Minima S4", "min": 0, "max": 100, "initial_value": 50, "tick_interval": 10},
            {"type": "slider", "name": "Tonalidad Maxima S4", "min": 0, "max": 200, "initial_value": 100, "tick_interval": 20},
            {"type": "slider", "name": "Pureza Minima S4", "min": 0, "max": 50, "initial_value": 25, "tick_interval": 5},
            {"type": "slider", "name": "Pureza Maxima S4", "min": 0, "max": 50, "initial_value": 25, "tick_interval": 5},
            {"type": "slider", "name": "Luminosidad Minima S4", "min": 0, "max": 100, "initial_value": 50, "tick_interval": 10},
            {"type": "slider", "name": "Luminosidad Maxima S4", "min": 0, "max": 200, "initial_value": 100, "tick_interval": 20},
            {"type": "slider", "name": "Kernel X S4", "min": 0, "max": 50, "initial_value": 25, "tick_interval": 5},
            {"type": "slider", "name": "Kernel Y S4", "min": 0, "max": 50, "initial_value": 25, "tick_interval": 5}
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
