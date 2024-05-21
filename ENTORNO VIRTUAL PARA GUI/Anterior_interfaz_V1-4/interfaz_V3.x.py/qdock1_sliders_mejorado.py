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
                            QComboBox)
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









        #Filtro1------------------------------------------------------------
        self.Filtro1 = QWidget()
        contenedor_filtro1 = QVBoxLayout()
        #filtro2---------------------------------------------------------------
        self.Filtro2 = QWidget()
        contenedor_filtro2 = QVBoxLayout()
        #filtro3---------------------------------------------------------------
        self.Filtro3 = QWidget()
        contenedor_filtro3 = QVBoxLayout()
        #filtro3---------------------------------------------------------------
        self.Filtro4 = QWidget()
        contenedor_filtro4 = QVBoxLayout()

        contenedor_filtro1.setSpacing(0)
        self.Filtro1.setLayout(contenedor_filtro1)

        contenedor_filtro2.setSpacing(0)
        self.Filtro2.setLayout(contenedor_filtro2)

        contenedor_filtro3.setSpacing(0)
        self.Filtro3.setLayout(contenedor_filtro3)

        contenedor_filtro4.setSpacing(0)
        self.Filtro4.setLayout(contenedor_filtro4)



        tab_bar_filtro_RGB = QTabWidget()
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

    

    ###Aqui termina la parte de la interfaz
    
    ###Primer intento añadir video
    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = Ventana_Principal()
    sys.exit(app.exec())
