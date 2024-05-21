import multiprocessing
import sys
from PyQt6.QtWidgets import (QApplication,
                            QWidget,
                            QLabel,
                            QLineEdit,
                            QPushButton,
                            QMainWindow,
                            QDockWidget,
                            QStatusBar,
                            QHBoxLayout,
                            QVBoxLayout,
                            QTabWidget,
                            QMainWindow,
                            QGridLayout,
                            QSlider,
                            QComboBox,
                            QTableWidget,
                            QTableWidgetItem,
                            QHeaderView,
                            QRadioButton,
                            QCheckBox)

from PyQt6.QtGui import QImage, QPixmap,QAction,QKeySequence,QGuiApplication, QScreen,QFont
from PyQt6.QtCore import Qt,QThread, pyqtSignal, QMutex, QMutexLocker,QTimer,QCoreApplication,QObject
import cv2
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button, TextBox
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import time
from queue import Queue
import cv2.aruco as aruco
import random
import serial
#multiprocessing.set_start_method('spawn')

width_video_capture = int
height_video_capture = int


class VideoStreamThread(QThread):
    frame_actualizado = pyqtSignal(QImage)
    finalizado = pyqtSignal()
    frame_captured = pyqtSignal(np.ndarray)
    
    
    def __init__(self,input_queue_ROI1,input_queue_ROI2,input_queue_ROI3,input_queue_ROI4,imagen_proyeccion):
        super().__init__()
        self.fla1 = True
        self.capturando = False
        self.pausado = False
        self.latest_frame = None
        self.frame_lock = QMutex()
        self.imagen_proyeccion = imagen_proyeccion
        self.O_ROI_1x = None
        self.O_ROI_1y = None
        self.O_ROI_2x = None
        self.O_ROI_2y = None
        self.O_ROI_3x = None
        self.O_ROI_3y = None
        self.O_ROI_4x = None
        self.O_ROI_4y = None
        self.WH_ROI_1x = None
        self.WH_ROI_1y = None
        self.WH_ROI_2x = None
        self.WH_ROI_2y = None
        self.WH_ROI_3x = None
        self.WH_ROI_3y = None
        self.WH_ROI_4x = None
        self.WH_ROI_4y = None
        self.input_queue_ROI1 = input_queue_ROI1 
        self.input_queue_ROI2 = input_queue_ROI2
        self.input_queue_ROI3 = input_queue_ROI3
        self.input_queue_ROI4 = input_queue_ROI4
        self.frame_ROI_1 = pyqtSignal(np.ndarray)
        self.frame_ROI_2 = pyqtSignal(np.ndarray)
        self.frame_ROI_3 = pyqtSignal(np.ndarray)
        self.frame_ROI_4 = pyqtSignal(np.ndarray)
        self.iniciar_captura_frame_ROI1 = False
        self.iniciar_captura_frame_ROI2 = False
        self.iniciar_captura_frame_ROI3 = False
        self.iniciar_captura_frame_ROI4 = False
        self.input_queue_Valores_estaticos = multiprocessing.Queue(maxsize= 1)
        self.input_queue_Valores_Variables = multiprocessing.Queue(maxsize= 1)

       
            
    def get_latest_frame(self):
        with QMutexLocker(self.frame_lock):
            return self.latest_frame if self.latest_frame is not None else None

    def run(self):
        try:
            coordinate_image_initialized = False
            coordinate_image = None
            Yatengodatos = True
            self.capturando = True
            #cv2.setUseOptimized(False)
            video_stream = cv2.VideoCapture(0)
            
            if Yatengodatos:
                global width_video_capture, height_video_capture
                width_video_capture = int(video_stream.get(cv2.CAP_PROP_FRAME_WIDTH))
                height_video_capture = int(video_stream.get(cv2.CAP_PROP_FRAME_HEIGHT))
                Yatengodatos = False
                #print(f"Resolución de la cámara: {width_video_capture}x{height_video_capture}")
            if not coordinate_image_initialized:
                    coordinate_image = self.create_cartesian_plane_custom(width_video_capture, height_video_capture, 50, 0, 0)
                    coordinate_image_initialized = True

            while self.capturando:
                ret, frame = video_stream.read()

                if not ret:
                    raise Exception(f"Error al capturar el fotograma: {video_stream.get(cv2.CAP_PROP_FRAME_WIDTH)} x {video_stream.get(cv2.CAP_PROP_FRAME_HEIGHT)}")

                with QMutexLocker(self.frame_lock):
                    self.latest_frame = frame
                    #print("frame copiado y enviado")
                self.lastest_frame = frame
                try:
                    self.imagen_proyeccion.put_nowait(self.lastest_frame)
                except:
                    pass
                self.frame_video_ventanacentral = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                if self.O_ROI_1x is not None and self.O_ROI_1y is not None and self.WH_ROI_1x is not None and self.WH_ROI_1y is not None:
                    cv2.rectangle(self.frame_video_ventanacentral, (self.O_ROI_1x, self.O_ROI_1y), (self.O_ROI_1x + self.WH_ROI_1x, self.O_ROI_1y + self.WH_ROI_1y), (205, 6, 35), 2)
                    if self.iniciar_captura_frame_ROI1 is True:
                        frame_ROI_1 = frame[self.O_ROI_1y:self.O_ROI_1y+self.WH_ROI_1y, self.O_ROI_1x:self.O_ROI_1x+self.WH_ROI_1x]
                        if not self.input_queue_ROI1.full():
                            self.input_queue_ROI1.put(frame_ROI_1)
                        
                if self.O_ROI_2x is not None and self.O_ROI_2y is not None and self.WH_ROI_2x is not None and self.WH_ROI_2y is not None:
                    cv2.rectangle(self.frame_video_ventanacentral, (self.O_ROI_2x, self.O_ROI_2y), (self.O_ROI_2x + self.WH_ROI_2x, self.O_ROI_2y + self.WH_ROI_2y), (245, 250, 7), 2)
                    if self.iniciar_captura_frame_ROI2 is True:
                        frame_ROI_2 = frame[self.O_ROI_2y:self.O_ROI_2y+self.WH_ROI_2y, self.O_ROI_2x:self.O_ROI_2x+self.WH_ROI_2x]
                        if not self.input_queue_ROI2.full():
                            self.input_queue_ROI2.put(frame_ROI_2)
                    
                if self.O_ROI_3x is not None and self.O_ROI_3y is not None and self.WH_ROI_3x is not None and self.WH_ROI_3y is not None:
                    cv2.rectangle(self.frame_video_ventanacentral, (self.O_ROI_3x, self.O_ROI_3y), (self.O_ROI_3x + self.WH_ROI_3x, self.O_ROI_3y + self.WH_ROI_3y), (7, 250, 42), 2)
                    if self.iniciar_captura_frame_ROI3 is True:
                        frame_ROI_3 = frame[self.O_ROI_3y:self.O_ROI_3y+self.WH_ROI_3y, self.O_ROI_3x:self.O_ROI_3x+self.WH_ROI_3x]
                        if not self.input_queue_ROI3.full():
                            self.input_queue_ROI3.put(frame_ROI_3)
                    
                if self.O_ROI_4x is not None and self.O_ROI_4y is not None and self.WH_ROI_4x is not None and self.WH_ROI_4y is not None:
                    cv2.rectangle(self.frame_video_ventanacentral, (self.O_ROI_4x, self.O_ROI_4y), (self.O_ROI_4x + self.WH_ROI_4x, self.O_ROI_4y + self.WH_ROI_4y), (7, 15, 250), 2)
                    if self.iniciar_captura_frame_ROI4 is True:
                        frame_ROI_4 = frame[self.O_ROI_4y:self.O_ROI_4y+self.WH_ROI_4y, self.O_ROI_4x:self.O_ROI_4x+self.WH_ROI_4x]
                        if not self.input_queue_ROI4.full():
                            self.input_queue_ROI4.put(frame_ROI_4)

                global cords_ROI_1,cords_ROI_2, cords_ROI_3, cords_ROI_4,cm_ancho_entre_puntos,cm_alto_entre_puntos,camera_matrix,distortion_parameters,Dictvect,flag_creacion_3D
                try:    
                    if cords_ROI_1 is not None and cords_ROI_2 is not None and cords_ROI_3 is not None and cords_ROI_4  is not None:
                        #Antes de esto crear la actualizacion de los diccionarios y el envio por queues
                        rect_coords = np.array([cords_ROI_1, cords_ROI_3, cords_ROI_4,cords_ROI_2])
                        cv2.polylines(self.frame_video_ventanacentral, [rect_coords], isClosed=True, color=(0, 0, 255), thickness=2)
                        flag_creacion_3D = True
    
                except:
                    print("error en creacion de rectanulo objeto")
                combined_image = self.overlay_images(self.frame_video_ventanacentral, coordinate_image)
                q_image = QImage(combined_image.data, width_video_capture, height_video_capture, width_video_capture * 3, QImage.Format.Format_RGB888)
                self.frame_actualizado.emit(q_image)

                QThread.msleep(30)
                #fin_iteracion = time.time()
            QThread.msleep(30)
            #duracion_iteracion = fin_iteracion - inicio_iteracion
            #tasa_de_fps_aprox = 1/duracion_iteracion
            #print(f'tasa de fps aprox: {tasa_de_fps_aprox} fps')

        except Exception as e:
            print(f"Excepción en el hilo de ejecución 1: {e}")
        finally:
            self.iniciar_captura_frame_ROI1 = False
            self.iniciar_captura_frame_ROI2 = False
            self.iniciar_captura_frame_ROI3 = False
            self.iniciar_captura_frame_ROI4 = False

            video_stream.release()
            self.finalizado.emit()
            print("videostreamtread finalizado")


    
        
            
    def Iniciar_captura_frame_ROI1(self):
        self.iniciar_captura_frame_ROI1 = True
        
    def parar_captura_frame_ROI1(self):
        self.iniciar_captura_frame_ROI1 = False
        print("se finalizo la captura del ROI1")

    def Iniciar_captura_frame_ROI2(self):
        self.iniciar_captura_frame_ROI2 = True
        
    def parar_captura_frame_ROI2(self):
        self.iniciar_captura_frame_ROI2 = False
        print("se finalizo la captura del ROI1")

    def Iniciar_captura_frame_ROI3(self):
        self.iniciar_captura_frame_ROI3 = True
        
    def parar_captura_frame_ROI3(self):
        self.iniciar_captura_frame_ROI3 = False
        print("se finalizo la captura del ROI1")

    def Iniciar_captura_frame_ROI4(self):
        self.iniciar_captura_frame_ROI4 = True

    def parar_captura_frame_ROI4(self):
        self.iniciar_captura_frame_ROI4 = False
        print("se finalizo la captura del ROI1") 

    def create_cartesian_plane_custom(self, roi_width, roi_height, scale, Inicio_px_X, Inicio_px_Y):
        # Calcula las dimensiones del plano cartesiano según las dimensiones de la ROI
        width = roi_width
        height = roi_height
        image = np.zeros((height, width, 3), dtype=np.uint8)

        # Dibuja los ejes X e Y
        cv2.line(image, (0, height - 1), (width - 1, height - 1), (85, 0, 174), 2)
        cv2.line(image, (0, 0), (0, height - 1), (85, 0, 174), 2)

        # Dibuja las marcas cada `scale` píxeles en los ejes y las etiquetas con las coordenadas

        for x in range(0, width, scale):
            cv2.line(image, (x, 0), (x, 6), (85, 0, 174), 2)
            cv2.putText(image, str(x + Inicio_px_X), (x, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (85, 0, 174), 2)

        for y in range(0, height, scale):
            cv2.line(image, (0, y), (5, y), (85, 0, 174), 2)
            cv2.putText(image, str(y + Inicio_px_Y), (8, y + 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (85, 0, 174), 2)

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
    
    def crear_rectanulo_ROI1(self,roi_x, roi_y, roi_width, roi_height):
        self.O_ROI_1x = roi_x
        self.O_ROI_1y = roi_y
        self.WH_ROI_1x = roi_width
        self.WH_ROI_1y = roi_height
            
    def crear_rectanulo_ROI2(self, roi_x, roi_y, roi_width, roi_height):

        self.O_ROI_2x = roi_x
        self.O_ROI_2y = roi_y
        self.WH_ROI_2x = roi_width
        self.WH_ROI_2y = roi_height

    def crear_rectanulo_ROI3(self, roi_x, roi_y, roi_width, roi_height):

        self.O_ROI_3x = roi_x
        self.O_ROI_3y = roi_y
        self.WH_ROI_3x = roi_width
        self.WH_ROI_3y = roi_height

    def crear_rectanulo_ROI4(self, roi_x, roi_y, roi_width, roi_height):

        self.O_ROI_4x = roi_x
        self.O_ROI_4y = roi_y
        self.WH_ROI_4x = roi_width
        self.WH_ROI_4y = roi_height

    def detener_captura(self):
        self.capturando = False
   
    def stop(self):
        self.quit()  # This will exit the thread's event loop
        self.wait()  



        

class VideoWidget(QWidget):
    
    def __init__(self,dic_thread,hilo_video,midockwiet):
        super().__init__()
        self.dic_thread = dic_thread
        self.hilo_video = hilo_video
        self.midockwiet = midockwiet

        self.table_data_ROI = {}
        self.table_widget = QTableWidget(4, 4)  # 4 filas x 4 columnas
        datos = [
            ["0", "0", "210", "210"],
            ["0", "210",  "0", "210"],
            ["210", "210", "210","210"],
            ["210", "210", "210","210"]
        ]

        for i, fila in enumerate(datos):
            for j, valor in enumerate(fila):
                item = QTableWidgetItem(valor)
                self.table_widget.setItem(i, j, item)
        try:
            for i in range(4):
                item = QTableWidgetItem("ROI 1")
                item2 = QTableWidgetItem("ROI 2")
                item3 = QTableWidgetItem("ROI 3")
                item4 = QTableWidgetItem("ROI 4")
                item5 = QTableWidgetItem("ROI X")
                item6 = QTableWidgetItem("ROI Y")
                item7 = QTableWidgetItem("ROI Width")
                item8 = QTableWidgetItem("ROI Height")

                self.table_widget.setHorizontalHeaderItem(0, item)
                self.table_widget.setHorizontalHeaderItem(1, item2)
                self.table_widget.setHorizontalHeaderItem(2, item3)
                self.table_widget.setHorizontalHeaderItem(3, item4)
                self.table_widget.setVerticalHeaderItem(0, item5)
                self.table_widget.setVerticalHeaderItem(1, item6)
                self.table_widget.setVerticalHeaderItem(2, item7)
                self.table_widget.setVerticalHeaderItem(3, item8)

            self.table_widget.setMinimumSize(200, 146)
            self.table_widget.setMaximumSize(640,146)
            for col in range(self.table_widget.columnCount()):
                self.table_widget.horizontalHeader().setSectionResizeMode(col, QHeaderView.ResizeMode.Stretch)
            self.label_video = QLabel(self)
            layout = QVBoxLayout(self)
            
            layout.addWidget(self.table_widget)
            layout.addWidget(self.label_video)  # Adjust the row span for the video label
            layout.addStretch(1)
        except Exception as e:
            print(f"Error: {e}")
            
        # Emit the signal with the updated text
    def Actualizar_ROI_Dict(self):
        global width_video_capture,height_video_capture
# Iterar sobre las filas y columnas de la tabla
        for row in range(self.table_widget.rowCount()):
            for col in range(self.table_widget.columnCount()):
                item = self.table_widget.item(row, col)
                if item is not None:
                    # Almacenar el valor de la casilla en el diccionario
                    key = f"{row}{col}"
                    value = item.text()
                    self.table_data_ROI[key] = value
        try:
            O_ROI_1x = int(self.table_data_ROI.get("00")) if self.table_data_ROI.get("00") is not None else None
            O_ROI_1y = int(self.table_data_ROI.get("10")) if self.table_data_ROI.get("10") is not None else None
            O_ROI_2x = int(self.table_data_ROI.get("01")) if self.table_data_ROI.get("01") is not None else None
            O_ROI_2y = int(self.table_data_ROI.get("11")) if self.table_data_ROI.get("11") is not None else None
            O_ROI_3x = int(self.table_data_ROI.get("02")) if self.table_data_ROI.get("02") is not None else None
            O_ROI_3y = int(self.table_data_ROI.get("12")) if self.table_data_ROI.get("12") is not None else None
            O_ROI_4x = int(self.table_data_ROI.get("03")) if self.table_data_ROI.get("03") is not None else None
            O_ROI_4y = int(self.table_data_ROI.get("13")) if self.table_data_ROI.get("13") is not None else None
            WH_ROI_1x = int(self.table_data_ROI.get("20")) if self.table_data_ROI.get("20") is not None else None
            WH_ROI_1y = int(self.table_data_ROI.get("30")) if self.table_data_ROI.get("30") is not None else None
            WH_ROI_2x = int(self.table_data_ROI.get("21")) if self.table_data_ROI.get("21") is not None else None
            WH_ROI_2y = int(self.table_data_ROI.get("31")) if self.table_data_ROI.get("31") is not None else None
            WH_ROI_3x = int(self.table_data_ROI.get("22")) if self.table_data_ROI.get("22") is not None else None
            WH_ROI_3y = int(self.table_data_ROI.get("32")) if self.table_data_ROI.get("32") is not None else None
            WH_ROI_4x = int(self.table_data_ROI.get("23")) if self.table_data_ROI.get("23") is not None else None
            WH_ROI_4y = int(self.table_data_ROI.get("33")) if self.table_data_ROI.get("33") is not None else None
            
            
            if all(isinstance(val, int) for val in [O_ROI_1x, O_ROI_1y, WH_ROI_1x, WH_ROI_1y,width_video_capture,height_video_capture]):
                if O_ROI_1x<width_video_capture and O_ROI_1y<height_video_capture and WH_ROI_1x<(width_video_capture-O_ROI_1x) and WH_ROI_1y<(height_video_capture-O_ROI_1y):
                    self.O_ROI_1 = (O_ROI_1x,O_ROI_1y)
                    self.WH_ROI_1 = (WH_ROI_1x,WH_ROI_1y)
                    self.dic_thread.manejar_actualizacion_cords("Origen de ROI color 1 X",O_ROI_1x)
                    self.dic_thread.manejar_actualizacion_cords("Origen de ROI color 1 Y",O_ROI_1y)
                    self.dic_thread.manejar_actualizacion_cords("width_height ROI color 1 X",WH_ROI_1x)
                    self.dic_thread.manejar_actualizacion_cords("width_height ROI color 1 Y",WH_ROI_1y)
                    self.hilo_video.crear_rectanulo_ROI1(O_ROI_1x, O_ROI_1y, WH_ROI_1x, WH_ROI_1y)
                    self.midockwiet.image_processor_thread.Iniciar_process1()
                else:
                    print("La columna 1 no tiene rangos correctos")
            else:
                print("la columna 1 no contiene todos los datos como enteros")

            if all(isinstance(val, int) for val in [O_ROI_2x, O_ROI_2y, WH_ROI_2x, WH_ROI_2y,width_video_capture,height_video_capture]):
                if O_ROI_2x<width_video_capture and O_ROI_2y<height_video_capture and WH_ROI_2x<(width_video_capture-O_ROI_2x)and WH_ROI_2y<(height_video_capture-O_ROI_2y):
                    self.dic_thread.manejar_actualizacion_cords('Origen de ROI color 2 X',O_ROI_2x)
                    self.dic_thread.manejar_actualizacion_cords('Origen de ROI color 2 Y',O_ROI_2y)
                    self.dic_thread.manejar_actualizacion_cords('width_height ROI color 2 X',WH_ROI_2x)
                    self.dic_thread.manejar_actualizacion_cords('width_height ROI color 2 Y',WH_ROI_2y)
                    self.hilo_video.crear_rectanulo_ROI2(O_ROI_2x, O_ROI_2y, WH_ROI_2x, WH_ROI_2y)
                    self.midockwiet.image_processor_thread.Iniciar_process2()
                else:
                    print("La columna 2 no tiene datos correctos")
            else:
                print("la columna 2 no contiene todos los datos como enteros")
            if all(isinstance(val, int) for val in [O_ROI_3x, O_ROI_3y, WH_ROI_3x, WH_ROI_3y,width_video_capture,height_video_capture]):
                if O_ROI_3x<width_video_capture and O_ROI_3y<height_video_capture and WH_ROI_3x<(width_video_capture-O_ROI_3x)and WH_ROI_3y<(height_video_capture-O_ROI_3y):
                    self.dic_thread.manejar_actualizacion_cords('Origen de ROI color 3 X',O_ROI_3x)
                    self.dic_thread.manejar_actualizacion_cords('Origen de ROI color 3 Y',O_ROI_3y)
                    self.dic_thread.manejar_actualizacion_cords('width_height ROI color 3 X',WH_ROI_3x)
                    self.dic_thread.manejar_actualizacion_cords('width_height ROI color 3 Y',WH_ROI_3y)
                    self.hilo_video.crear_rectanulo_ROI3(O_ROI_3x, O_ROI_3y, WH_ROI_3x, WH_ROI_3y)
                    self.midockwiet.image_processor_thread.Iniciar_process3()
                else:
                    print("La columna 3 no tiene datos correctos")
                    
            else:
                print("la columna 3 no contiene todos los datos como enteros")
            if all(isinstance(val, int) for val in [O_ROI_4x, O_ROI_4y, WH_ROI_4x, WH_ROI_4y,width_video_capture,height_video_capture]):
                if O_ROI_4x<width_video_capture and O_ROI_4y<height_video_capture and WH_ROI_4x<(width_video_capture-O_ROI_4x)and WH_ROI_4y<(height_video_capture-O_ROI_4y):
                    self.dic_thread.manejar_actualizacion_cords('Origen de ROI color 4 X',O_ROI_4x)
                    self.dic_thread.manejar_actualizacion_cords('Origen de ROI color 4 Y',O_ROI_4y)
                    self.dic_thread.manejar_actualizacion_cords('width_height ROI color 4 X',WH_ROI_4x)
                    self.dic_thread.manejar_actualizacion_cords('width_height ROI color 4 Y',WH_ROI_4y)
                    self.hilo_video.crear_rectanulo_ROI4(O_ROI_4x, O_ROI_4y, WH_ROI_4x, WH_ROI_4y)
                    self.midockwiet.image_processor_thread.Iniciar_process4()
                else:
                        print("La columna 4 no tiene datos correctos")
            else:
                print("la columna 4 no contiene todos los datos como enteros")
        except Exception as e:
            print(f"Excepción en el hilo de ejecución 2: {e}")

    def actualizar_frame(self, q_image):
        try:    
            if q_image:
                pixmap = QPixmap.fromImage(q_image)
                margin = self.table_widget.width()
                pixmap = pixmap.scaledToWidth(margin-10)
                self.label_video.setPixmap(pixmap)
        except Exception as e:
            print(f"Excepción en el hilo de ejecución 3: {e}")
class MiVentana(QWidget):
    def __init__(self, video_thread,dic_thread,midockwiet):
        super().__init__()
        self.dic_thread = dic_thread
        self.hilo_video = video_thread
        self.midockwiet = midockwiet

        self.video_widget = VideoWidget(self.dic_thread,self.hilo_video, self.midockwiet)
        self.hilo_video.frame_actualizado.connect(self.video_widget.actualizar_frame)
        self.hilo_video.finalizado.connect(self.hilo_finalizado)

        layout_principal = QGridLayout(self)
        boton_iniciar = QPushButton("Iniciar Captura", self)
        boton_detener = QPushButton("Detener Captura", self)
        Actualizar_ROI = QPushButton("Actualizar_ROI", self)
        boton_iniciar.clicked.connect(self.iniciar_captura)
        boton_detener.clicked.connect(self.detener_captura)
        Actualizar_ROI.clicked.connect(self.Enviar_ROI)
        layout_principal.addWidget(self.video_widget, 1, 1, 1, 3)
        layout_principal.addWidget(boton_iniciar, 2, 1, 1, 1)
        layout_principal.addWidget(boton_detener, 2, 2, 1, 1)
        layout_principal.addWidget(Actualizar_ROI, 2, 3, 1, 1)

    def iniciar_captura(self):
        self.hilo_video.start()

    def detener_captura(self):
        self.midockwiet.stop_camera()
        self.hilo_video.detener_captura()
        

    def Enviar_ROI(self):
        self.video_widget.Actualizar_ROI_Dict()
        
    def hilo_finalizado(self):
        print("Captura finalizada")
class MiDockWidget(QWidget):
    def __init__(self, video_thread,dic_thread,input_queue_ROI1,input_queue_ROI2,input_queue_ROI3,input_queue_ROI4,parametros_vectores):
        super().__init__()
        self.input_queue_ROI1 = input_queue_ROI1
        self.input_queue_ROI2 = input_queue_ROI2
        self.input_queue_ROI3 = input_queue_ROI3
        self.input_queue_ROI4 = input_queue_ROI4
        self.parametros_vectores = parametros_vectores
        self.dic_thread = dic_thread
        self.hilo_video = video_thread
        self.presets_combobox = QComboBox(self)
        self.presets_combobox.addItems(["Original", "Seleccion de colores", "Contornos"])
        self.presets_combobox.currentIndexChanged.connect(self.on_preset_changed)
        # Crear instancia de ImageProcessorThread y pasarla a MiDockWidget
        self.image_processor_thread = ImageProcessorThread(self.hilo_video.get_latest_frame,self.dic_thread,self.input_queue_ROI1,self.input_queue_ROI2,self.input_queue_ROI3,self.input_queue_ROI4,self.hilo_video,self.parametros_vectores)
        
        self.label2 = QLabel(self)
        self.label3 = QLabel(self)
        self.label4 = QLabel(self)
        self.label5 = QLabel(self)

        layout_principalQD = QGridLayout(self)
        start_button_d = QPushButton("Iniciar Captura mascara", self)
        stop_button_d = QPushButton("Detener Captura mascara", self)

        layout_principalQD.addWidget(self.label2, 1, 1, 1, 1)
        layout_principalQD.addWidget(self.label3, 2, 1, 1, 1)
        layout_principalQD.addWidget(self.label4, 1, 2, 1, 1)
        layout_principalQD.addWidget(self.label5, 2, 2, 1, 1)

        layout_principalQD.addWidget(start_button_d, 4, 1, 1, 1)
        layout_principalQD.addWidget(stop_button_d, 4, 2, 1, 1)
        layout_principalQD.addWidget(self.presets_combobox, 5, 1, 1, 2)

        self.image_processor_thread.processed_frame_signal.connect(self.update_frame2)
        self.image_processor_thread.processed_frame_signal1.connect(self.update_frame3)
        self.image_processor_thread.processed_frame_signal2.connect(self.update_frame4)
        self.image_processor_thread.processed_frame_signal3.connect(self.update_frame5)

        self.timer = QTimer(self)
        self.timer.start(60)

        stop_button_d.clicked.connect(self.stop_camera)
        start_button_d.clicked.connect(self.start_camera)
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
        if self.hilo_video.isRunning() and not self.image_processor_thread.isRunning():
            self.image_processor_thread.start()

    def stop_camera(self):
        self.image_processor_thread.finalizar_process()
        self.image_processor_thread.stop1()

    


    def clear_labels(self):
        self.label2.clear()
        self.label3.clear()
        self.label4.clear()

    def closeEvent(self, event):
        self.timer.stop()




class ImageProcessorThread(QThread):
    processed_frame_signal = pyqtSignal(QImage)
    processed_frame_signal1 = pyqtSignal(QImage)
    processed_frame_signal2 = pyqtSignal(QImage)
    processed_frame_signal3 = pyqtSignal(QImage)
    pausar_signal = pyqtSignal()
    reanudar_signal = pyqtSignal()
    diccionario_del_IPT = dict
    O_ROI_1X = 0
    O_ROI_1Y = 0
    WH_ROI_1X = 0
    WH_ROI_1Y = 0
    O_ROI_2X = 0
    O_ROI_2Y = 0
    WH_ROI_2X = 0
    WH_ROI_2Y = 0
    O_ROI_3X = 0
    O_ROI_3Y = 0
    WH_ROI_3X = 0
    WH_ROI_3Y = 0
    O_ROI_4X = 0
    O_ROI_4Y = 0
    WH_ROI_4X = 0
    WH_ROI_4Y = 0
    output_queue_ROI1 = multiprocessing.Queue(maxsize = 5)
    output_queue_ROI2 = multiprocessing.Queue(maxsize = 5)
    output_queue_ROI3 = multiprocessing.Queue(maxsize = 5)
    output_queue_ROI4 = multiprocessing.Queue(maxsize = 5)
    DIC_Queue_ROI_1 = multiprocessing.Queue(maxsize = 1)
    DIC_Queue_ROI_2 = multiprocessing.Queue(maxsize = 1)
    DIC_Queue_ROI_3 = multiprocessing.Queue(maxsize = 1)
    DIC_Queue_ROI_4 = multiprocessing.Queue(maxsize = 1)
    DIC_Result_queue_ROI1 = multiprocessing.Queue(maxsize = 1)
    DIC_Result_queue_ROI2 = multiprocessing.Queue(maxsize = 1)
    DIC_Result_queue_ROI3 = multiprocessing.Queue(maxsize = 1)
    DIC_Result_queue_ROI4 = multiprocessing.Queue(maxsize = 1)
    

    
    def __init__(self, get_frame_function, dic_thread,input_queue_ROI1,input_queue_ROI2,input_queue_ROI3,input_queue_ROI4,hilo_video,parametros_vectores):
        super().__init__()
        self.input_queue_ROI1 = input_queue_ROI1
        self.input_queue_ROI2 = input_queue_ROI2
        self.input_queue_ROI3 = input_queue_ROI3
        self.input_queue_ROI4 = input_queue_ROI4
        self.parametros_vectores = parametros_vectores
        self.hilo_video = hilo_video
        
        self.dic_thread = dic_thread
        self.dic_thread.enviar_signal.connect(self.actualizar_dic_IPT)
        self.get_frame_function = get_frame_function
        # Inicializar el preset actual
        self.current_preset = "Original"
        self.process_flag_1 = False
        self.process_flag_2 = False
        self.process_flag_3 = False
        self.process_flag_4 = False
        global camera_matrix,distortion_parameters
        self.process_1 = VideoProcess(self.input_queue_ROI1,self.output_queue_ROI1,self.DIC_Queue_ROI_1,self.DIC_Result_queue_ROI1,1,camera_matrix,distortion_parameters)
        self.Bucle_frames_processados_1 = VideoProcessingThread(self.output_queue_ROI1,self.processed_frame_signal,self.DIC_Result_queue_ROI1,1,self.parametros_vectores)
        self.process_2 = VideoProcess(self.input_queue_ROI2,self.output_queue_ROI2,self.DIC_Queue_ROI_2,self.DIC_Result_queue_ROI2,2,camera_matrix,distortion_parameters)
        self.Bucle_frames_processados_2 = VideoProcessingThread(self.output_queue_ROI2,self.processed_frame_signal1,self.DIC_Result_queue_ROI2,2,self.parametros_vectores)
        self.process_3 = VideoProcess(self.input_queue_ROI3,self.output_queue_ROI3,self.DIC_Queue_ROI_3,self.DIC_Result_queue_ROI3,3,camera_matrix,distortion_parameters)
        self.Bucle_frames_processados_3 = VideoProcessingThread(self.output_queue_ROI3,self.processed_frame_signal2,self.DIC_Result_queue_ROI3,3,self.parametros_vectores)
        self.process_4 = VideoProcess(self.input_queue_ROI4,self.output_queue_ROI4,self.DIC_Queue_ROI_4,self.DIC_Result_queue_ROI4,4,camera_matrix,distortion_parameters)
        self.Bucle_frames_processados_4 = VideoProcessingThread(self.output_queue_ROI4,self.processed_frame_signal3,self.DIC_Result_queue_ROI4,4,self.parametros_vectores)




        
##########################################################################aqui se conectan los sliders

    def run(self):
        
        while not self.isInterruptionRequested():
            frame = self.get_frame_function()
            if frame is not None and frame.size != 0:
                if self.current_preset == "Original":
                    #print("se Inicio Original")       
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
                    
                    if self.process_flag_1:
                        
                        try:
                            if not self.process_1.is_alive() and self.process_1 is not None:
                                    self.process_1.start()
                        except Exception as e:
                            print(f"No se pudo iniciar process 1: {e}")
                        try:
                            if not self.Bucle_frames_processados_1.isRunning() and self.Bucle_frames_processados_1 is not None:
                                self.Bucle_frames_processados_1.start()
                        except Exception as e:
                            print(f"No se pudo iniciar Bucle_frames_processados_1: {e}")

                            
                        
                    if self.process_flag_2:
                        
                        try:
                            if not self.process_2.is_alive() and self.process_2 is not None:
                                    self.process_2.start()
                        except Exception as e:
                            print(f"No se pudo iniciar process 2: {e}")
                            #self.finalizar_process()
                        try:
                            if not self.Bucle_frames_processados_2.isRunning() and self.Bucle_frames_processados_2 is not None:
                                self.Bucle_frames_processados_2.start()
                        except Exception as e:
                            print(f"No se pudo iniciar Bucle_frames_processados_2: {e}")

                    
                    if self.process_flag_3:
                        
                        try:
                            if not self.process_3.is_alive() and self.process_3 is not None:
                                    self.process_3.start()
                        except Exception as e:
                            print(f"No se pudo iniciar process 3: {e}")
                        try:
                            if not self.Bucle_frames_processados_3.isRunning() and self.Bucle_frames_processados_3 is not None:
                                self.Bucle_frames_processados_3.start()
                        except Exception as e:
                            print(f"No se pudo iniciar Bucle_frames_processados_3: {e}")

                        
                    if self.process_flag_4:
                        
                        try:
                            if not self.process_4.is_alive() and self.process_4 is not None:
                                    self.process_4.start()
                        except Exception as e:
                            print(f"No se pudo iniciar process 4: {e}")
                            #self.finalizar_process()
                        try:
                            if not self.Bucle_frames_processados_4.isRunning() and self.Bucle_frames_processados_4 is not None:
                                self.Bucle_frames_processados_4.start()
                        except Exception as e:
                            print(f"No se pudo iniciar Bucle_frames_processados_4: {e}")
                    
                    time.sleep(5)

                elif self.current_preset == "Contornos":
                   pass
                QThread.msleep(60)
        print("ImageProcessorThread Finalizado")

    def Iniciar_process1(self):
        print("Iniciar process 1")
        self.hilo_video.Iniciar_captura_frame_ROI1()
        self.process_flag_1 = True        

    def Iniciar_process2(self):
        print("Iniciar process 2")
        self.process_flag_2 = True
        self.hilo_video.Iniciar_captura_frame_ROI2()

    def Iniciar_process3(self):
        print("Iniciar process 3")
        self.process_flag_3 = True
        self.hilo_video.Iniciar_captura_frame_ROI3()

    def Iniciar_process4(self):
        print("Iniciar process 4")
        self.process_flag_4 = True
        self.hilo_video.Iniciar_captura_frame_ROI4()

    def finalizar_process(self):
        print("Se inicio finalizar process")
        self.process_flag_1 = False
        self.process_flag_2 = False
        self.process_flag_3 = False
        self.process_flag_4 = False
        try: 
            if self.Bucle_frames_processados_1 is not None and self.Bucle_frames_processados_1.is_alive():
                self.Bucle_frames_processados_1.finalizar_process_interno()
                #self.Bucle_frames_processados_1.terminate()
                self.Bucle_frames_processados_1.wait()
                if self.Bucle_frames_processados_1 is not None and self.Bucle_frames_processados_1.is_alive():
                    print("No se finalizo el Bucle_frames_processados_1")
                else:
                    print("Se finalizo correctamente el Bucle_frames_processados_1")
            else:
                print("No esta activo el Bucle_frames_processados_1")
        except:
            pass
        try: 
            if self.Bucle_frames_processados_2 is not None and self.Bucle_frames_processados_2.is_alive():
                self.Bucle_frames_processados_2.finalizar_process_interno()
                #self.Bucle_frames_processados_2.terminate()
                self.Bucle_frames_processados_2.wait()
                if self.Bucle_frames_processados_2 is not None and self.Bucle_frames_processados_2.is_alive():
                    print("No se finalizo el Bucle_frames_processados_2")
                else:
                    print("Se finalizo correctamente el Bucle_frames_processados_2")
            else:
                print("No esta activo el Bucle_frames_processados_2")
        except:
            pass
        try: 
            if self.Bucle_frames_processados_3 is not None and self.Bucle_frames_processados_3.is_alive():
                self.Bucle_frames_processados_3.finalizar_process_interno()
                #self.Bucle_frames_processados_3.terminate()
                self.Bucle_frames_processados_3.wait()
                if self.Bucle_frames_processados_3 is not None and self.Bucle_frames_processados_3.is_alive():
                    print("No se finalizo el Bucle_frames_processados_3")
                else:
                    print("Se finalizo correctamente el Bucle_frames_processados_3")
            else:
                print("No esta activo el Bucle_frames_processados_3")
        except:
            pass
        try: 
            if self.Bucle_frames_processados_4 is not None and self.Bucle_frames_processados_4.is_alive():
                self.Bucle_frames_processados_4.finalizar_process_interno()
                #self.Bucle_frames_processados_4.terminate()
                self.Bucle_frames_processados_4.wait()
                if self.Bucle_frames_processados_4 is not None and self.Bucle_frames_processados_4.is_alive():
                    print("No se finalizo el Bucle_frames_processados_4")
                else:
                    print("Se finalizo correctamente el Bucle_frames_processados_4")
            else:
                print("No esta activo el Bucle_frames_processados_4")
        except:
            pass
        try: 
            if self.process_1 is not None and self.process_1.is_alive():
                self.process_1.finalizar_process_interno()
                self.process_1.terminate()
                self.process_1.join()
                print("Se finalizo correctamente el process 1")
                if self.process_1 is not None and self.process_1.is_alive():
                    print("No se finalizo el process 1")
                else:
                    print("Se finalizo correctamente el process 1")
            else:
                print("No esta activo el process 1")
        except:
            pass
        try:
            if self.process_2 is not None and self.process_2.is_alive():
                self.process_2.finalizar_process_interno()
                self.process_2.terminate()
                self.process_2.join()
                print("Se finalizo correctamente el process 2")
                if self.process_2 is not None and self.process_2.is_alive():
                    print("No se finalizo el process 2")
                else:
                    print("Se finalizo correctamente el process 2")
            else:
                print("No esta activo el process 2")
        except:
            pass
        try:
            if self.process_3 is not None and self.process_3.is_alive():
                self.process_3.finalizar_process_interno()
                self.process_3.terminate()
                self.process_3.join()
                print("Se finalizo correctamente el process 3")
                if self.process_3 is not None and self.process_3.is_alive():
                    print("No se finalizo el process 3")
                else:
                    print("Se finalizo correctamente el process 3")
            else:
                print("No esta activo el process 3")
        except:
            pass
        try:       
            if self.process_4 is not None and self.process_4.is_alive():
                self.process_4.finalizar_process_interno()
                self.process_4.terminate()
                self.process_4.join()
                print("Se finalizo correctamente el process 4")
                if self.process_4 is not None and self.process_4.is_alive():
                    print("No se finalizo el process 4")
                else:
                    print("Se finalizo correctamente el process 4")
            else:
                print("No esta activo el process 4")
        except:
            pass
       
    def actualizar_dic_IPT(self,diccionario):
        self.diccionario_del_IPT = diccionario


        self.O_ROI_1X = self.diccionario_del_IPT.get("Origen de ROI color 1 X")
        self.O_ROI_1Y = self.diccionario_del_IPT.get("Origen de ROI color 1 Y")
        self.WH_ROI_1X = self.diccionario_del_IPT.get("width_height ROI color 1 X")
        self.WH_ROI_1Y = self.diccionario_del_IPT.get("width_height ROI color 1 Y")


        self.O_ROI_2X = self.diccionario_del_IPT.get("Origen de ROI color 2 X")
        self.O_ROI_2Y = self.diccionario_del_IPT.get("Origen de ROI color 2 Y")
        self.WH_ROI_2X = self.diccionario_del_IPT.get("width_height ROI color 2 X")
        self.WH_ROI_2Y = self.diccionario_del_IPT.get("width_height ROI color 2 Y")



        self.O_ROI_3X = self.diccionario_del_IPT.get("Origen de ROI color 3 X")
        self.O_ROI_3Y = self.diccionario_del_IPT.get("Origen de ROI color 3 Y")
        self.WH_ROI_3X = self.diccionario_del_IPT.get("width_height ROI color 3 X")
        self.WH_ROI_3Y = self.diccionario_del_IPT.get("width_height ROI color 3 Y")


        self.O_ROI_4X = self.diccionario_del_IPT.get("Origen de ROI color 4 X")
        self.O_ROI_4Y = self.diccionario_del_IPT.get("Origen de ROI color 4 Y")
        self.WH_ROI_4X = self.diccionario_del_IPT.get("width_height ROI color 4 X")
        self.WH_ROI_4Y = self.diccionario_del_IPT.get("width_height ROI color 4 Y")

        if all(v != 0 for v in [self.WH_ROI_1X,self.WH_ROI_1Y]):
            self.diccionario_ROI_1 = {
            'O_ROI_X': self.O_ROI_1X,
            'O_ROI_Y': self.O_ROI_1Y,
            'WH_ROI_X': self.WH_ROI_1X,
            'WH_ROI_Y': self.WH_ROI_1Y,
            }  
            if not self.DIC_Queue_ROI_1.full():
                self.DIC_Queue_ROI_1.put(self.diccionario_ROI_1)
                #print("Se envio dic_ROI_1")
        if all(v != 0 for v in [self.WH_ROI_2X, self.WH_ROI_2Y]):
            self.diccionario_ROI_2 = {

                'O_ROI_X': self.O_ROI_2X,
                'O_ROI_Y': self.O_ROI_2Y,
                'WH_ROI_X': self.WH_ROI_2X,
                'WH_ROI_Y': self.WH_ROI_2Y,
            }  
            if not self.DIC_Queue_ROI_2.full():
                self.DIC_Queue_ROI_2.put(self.diccionario_ROI_2)

        if all(v != 0 for v in [self.WH_ROI_3X, self.WH_ROI_3Y]):
            self.diccionario_ROI_3 = {
  
                'O_ROI_X': self.O_ROI_3X,
                'O_ROI_Y': self.O_ROI_3Y,
                'WH_ROI_X': self.WH_ROI_3X,
                'WH_ROI_Y': self.WH_ROI_3Y,
            }  
            if not self.DIC_Queue_ROI_3.full():
                self.DIC_Queue_ROI_3.put(self.diccionario_ROI_3)

        if all(v != 0 for v in [self.WH_ROI_4X, self.WH_ROI_4Y]):
            self.diccionario_ROI_4 = {

                'O_ROI_X': self.O_ROI_4X,
                'O_ROI_Y': self.O_ROI_4Y,
                'WH_ROI_X': self.WH_ROI_4X,
                'WH_ROI_Y': self.WH_ROI_4Y,
            }  
            if not self.DIC_Queue_ROI_4.full():
                self.DIC_Queue_ROI_4.put(self.diccionario_ROI_4)
                

    def set_selected_preset(self, preset):
        self.current_preset = preset

    def stop1(self):
        self.requestInterruption()
        self.wait()

    def pausar(self):
        self.pausar_signal.emit()

    def reanudar(self):
        self.reanudar_signal.emit()
        

class VideoProcess(multiprocessing.Process):
    def __init__(self,input_queue_ROI,output_queue_ROI,DIC_Queue,DIC_Result_queue_ROI,int_valor_process,camera_matrix,distortion_parameters):
                
        super().__init__()
        self.input_queue = input_queue_ROI
        self.output_queue = output_queue_ROI
        self.DIC_Queue = DIC_Queue
        self.DIC_Result_queue_ROI = DIC_Result_queue_ROI
        self.int_valor_process = int_valor_process
        self.O_ROI_X = 0
        self.O_ROI_Y = 0
        self.WH_ROI_X = 0
        self.WH_ROI_Y = 0
        self.camera_matrix = camera_matrix 
        self.distortion_parameters = distortion_parameters
        self.detected_count = 0
        self.send_interval = 5
        
        
        self.process_flag_interno = True
        print("Init Videoprocess")

    def run(self):
        self.aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
        self.aruco_params = aruco.DetectorParameters()
        print("process iniciado")
        try:
            while self.process_flag_interno:
                if not self.DIC_Queue.empty():
                    self.ROI_DIC = self.DIC_Queue.get()
                   
                    if isinstance(self.ROI_DIC, dict):
                        self.O_ROI_X = self.ROI_DIC.get('O_ROI_X')
                        self.O_ROI_Y = self.ROI_DIC.get('O_ROI_Y')
                        self.WH_ROI_X = self.ROI_DIC.get('WH_ROI_X')
                        self.WH_ROI_Y = self.ROI_DIC.get('WH_ROI_Y')
                        #print(self.ROI_DIC)
                    else:
                        print("Se envio el dict pero no lo contiene los datos")

                if not self.input_queue.empty() and all(v != 0 for v in [self.WH_ROI_X,self.WH_ROI_Y]):
                    frame = self.input_queue.get()
                    self.detect_aruco_markers(frame, self.aruco_dict, self.aruco_params)
                    self.output_queue.put(frame)   
                    time.sleep(0.05)
                else:
                    time.sleep(0.2)
            else:
                    time.sleep(0.1)

        except Exception as e:
            print(f"Excepción en el process {self.int_valor_process}: {e}")
        print(f"Se Finalizo el process {self.int_valor_process}")
           
    def finalizar_process_interno(self):
        self.process_flag_interno = False
    def detect_aruco_markers(self,frame, aruco_dict, aruco_params):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=aruco_params)

        if ids is not None and corners is not None:
            aruco.drawDetectedMarkers(frame, corners, ids)
            corners_reales = []
            for esquina in corners:
                for punto in esquina[0]:
                    x, y = punto[0], punto[1]
                    corners_reales.append((int(x) + int(self.O_ROI_X), int(y) + int(self.O_ROI_Y)))
            if len(ids) > 0:
                rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners, 0.05, self.camera_matrix, self.distortion_parameters)
                self.Dict_pose = {"rvecs":rvecs,"tvecs":tvecs,"corners_reales":corners_reales}
                for i in range(len(ids)):
                        cv2.drawFrameAxes(frame, self.camera_matrix, self.distortion_parameters, rvecs[i], tvecs[i], 0.1)
                self.detected_count += 1
                if self.detected_count >= self.send_interval:
                    self.DIC_Result_queue_ROI.put(self.Dict_pose)
                    self.detected_count = 0
                
class VideoProcessingThread(QThread):
    def __init__(self,output_queue_ROI,processed_frame_signal,DIC_Result_queue_ROI,int_valor_process,parametros_vectores):
        super().__init__()
        self.output_queue_ROI = output_queue_ROI
        self.processed_frame_signal = processed_frame_signal
        self.DIC_Result_queue_ROI = DIC_Result_queue_ROI
        self.int_valor_process = int_valor_process
        self.parametros_vectores = parametros_vectores 
        self.flag_interno = True
    def run(self):
        while self.flag_interno:   
            try:   
                if not self.output_queue_ROI.empty():
                    frame_ROI_processed = self.output_queue_ROI.get()  
                    qt_ROI = QImage(frame_ROI_processed.data, frame_ROI_processed.shape[1], frame_ROI_processed.shape[0], frame_ROI_processed.strides[0], QImage.Format.Format_BGR888)#Format_Grayscale8
                    self.processed_frame_signal.emit(qt_ROI)
                    QThread.msleep(30)
                else:
                    QThread.msleep(30)
                if not self.DIC_Result_queue_ROI.empty():
                    self.actualizar_cordenadas(self.int_valor_process,self.DIC_Result_queue_ROI)
            except Exception as e:
                print(f"Excepción en el video tread {self.int_valor_process}: {e}")
    
        print("se finalizao el videdoprocessin tread")

    def actualizar_cordenadas(self, Valor_process,dic_roi):
        global cords_ROI_1,cords_ROI_2, cords_ROI_3, cords_ROI_4,flag_creacion_3D,Dictvect
        if Valor_process == 1:
            cords_dic_1 = dic_roi.get()
            rvecs_1 = cords_dic_1["rvecs"]
            tvecs_1 = cords_dic_1["tvecs"]
            corners_reales_1 = cords_dic_1["corners_reales"]
            cords_ROI_1 = corners_reales_1[1]
            if flag_creacion_3D:
                Dictvect["rvecs_1"] = rvecs_1
                Dictvect["tvecs_1"] = tvecs_1
                Dictvect["corners_reales_1"] = corners_reales_1
                Dictvect["tipo"] = str("parametros_vectores")
                
                try:
                    self.parametros_vectores.put_nowait(Dictvect)  # Intenta poner los datos en la cola sin esperar
                except:
                    pass
        elif Valor_process == 2:
            cords_dic_2 = dic_roi.get()
            rvecs_2 = cords_dic_2["rvecs"]
            tvecs_2 = cords_dic_2["tvecs"]
            corners_reales_2 = cords_dic_2["corners_reales"]
            cords_ROI_2 = corners_reales_2[0]
            if flag_creacion_3D:
                Dictvect["rvecs_2"] = rvecs_2
                Dictvect["tvecs_2"] = tvecs_2
                Dictvect["corners_reales_2"] = corners_reales_2
                Dictvect["tipo"] = str("parametros_vectores")
                try:
                    self.parametros_vectores.put_nowait(Dictvect)  # Intenta poner los datos en la cola sin esperar
                except:
                    pass
        elif Valor_process == 3:
            cords_dic_3 = dic_roi.get()
            rvecs_3 = cords_dic_3["rvecs"]
            tvecs_3 = cords_dic_3["tvecs"]
            corners_reales_3 = cords_dic_3["corners_reales"]
            cords_ROI_3 = corners_reales_3[2]
            if flag_creacion_3D:
                Dictvect["rvecs_3"] = rvecs_3
                Dictvect["tvecs_3"] = tvecs_3
                Dictvect["corners_reales_3"] = corners_reales_3
                Dictvect["tipo"] = str("parametros_vectores")
                try:
                    self.parametros_vectores.put_nowait(Dictvect)  # Intenta poner los datos en la cola sin esperar
                except:
                    pass
        elif Valor_process == 4:
            cords_dic_4 = dic_roi.get()
            rvecs_4 = cords_dic_4["rvecs"]
            tvecs_4 = cords_dic_4["tvecs"]
            corners_reales_4 = cords_dic_4["corners_reales"]
            cords_ROI_4 = corners_reales_4[3]
            if flag_creacion_3D:
                Dictvect["rvecs_4"] = rvecs_4
                Dictvect["tvecs_4"] = tvecs_4
                Dictvect["corners_reales_4"] = corners_reales_4
                Dictvect["tipo"] = str("parametros_vectores")
                try:
                    self.parametros_vectores.put_nowait(Dictvect)  # Intenta poner los datos en la cola sin esperar
                except:
                    pass
        

    def finalizar_process_interno(self):
        self.flag_interno = False
               

class DICThread(QThread):
    actualizar_signal = pyqtSignal(str, int)
    actualizar_signal_cords = pyqtSignal(str, int, int)
    enviar_signal = pyqtSignal(dict)
    def __init__(self):
        super().__init__()
        self.diccionario_datos = {"Origen de ROI color 1 X": 0, "Origen de ROI color 1 Y": 0,"width_height ROI color 1 X": 0,"width_height ROI color 1 Y": 0,
                                  "Origen de ROI color 2 X": 0, "Origen de ROI color 2 Y": 0,"width_height ROI color 2 X": 0,"width_height ROI color 2 Y": 0,
                                  "Origen de ROI color 3 X": 0, "Origen de ROI color 3 Y": 0,"width_height ROI color 3 X": 0,"width_height ROI color 3 Y": 0,
                                  "Origen de ROI color 4 X": 0, "Origen de ROI color 4 Y": 0,"width_height ROI color 4 X": 0,"width_height ROI color 4 Y": 0,
                                  }

    def run(self):
        self.actualizar_signal.connect(self.manejar_actualizacion)
        self.actualizar_signal_cords.connect(self.manejar_actualizacion_cords)

    def manejar_actualizacion(self, nombre, valor):
        #print(f"Nombre y valor almacenados en el hilo secundario - Nombre: {nombre}, Valor: {valor}")
        self.diccionario_datos[nombre] = valor
        self.enviar_signal.emit(self.diccionario_datos)
    
    def manejar_actualizacion_cords(self, nombre, valor):
        #print(f"Nombre y valor almacenados en el hilo secundario - Nombre: {nombre}, Valor: {valor}")
        self.diccionario_datos[nombre] = valor
        #print(str(nombre) +" : "+ str(valor))
    
        self.enviar_signal.emit(self.diccionario_datos)
        
    def stop(self):
        self.quit()  # This will exit the thread's event loop
        self.wait()
        print("dictread finalizado")  

class SerialThread(QThread):
    data_received = pyqtSignal(str)

    def __init__(self, port):
        super().__init__()
        self.port = port
        self.running = True

    def run(self):
        try:
            self.ser = serial.Serial(self.port, 9600, timeout=1)
            while self.running:
                if self.ser.in_waiting > 0:
                    data = self.ser.readline().decode('ascii').strip()
                    self.data_received.emit(data)
        except Exception as e:
            print(f"Error al leer del puerto serial: {e}")
        finally:
            self.ser.close()

    def stop(self):
        self.running = False
        self.wait()

class SerialControlWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.ser_thread = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Control de Botonera y Potenciómetros")
        self.setGeometry(100, 100, 600, 400)  # Ajustar tamaño para ser menos ancho

        grid_layout = QGridLayout(self)

        # Sliders para los potenciómetros
        self.sliders = {
            'Pot1': QSlider(Qt.Orientation.Horizontal),
            'Pot2': QSlider(Qt.Orientation.Horizontal)
        }
        self.sliders['Pot1'].setRange(0, 1023)
        self.sliders['Pot2'].setRange(0, 1023)
        grid_layout.addWidget(QLabel("Potenciómetro 1"), 0, 0)
        grid_layout.addWidget(self.sliders['Pot1'], 0, 1, 1, 6)  # Abarcar 6 columnas
        grid_layout.addWidget(QLabel("Potenciómetro 2"), 1, 0)
        grid_layout.addWidget(self.sliders['Pot2'], 1, 1, 1, 6)  # Abarcar 6 columnas

        # Conectar sliders al método emit_data_changed
        self.sliders['Pot1'].valueChanged.connect(self.emit_data_changed1)
        self.sliders['Pot2'].valueChanged.connect(self.emit_data_changed1)

        # Botones para entradas digitales con nombres específicos
        self.buttons = {}
        button_names = [
            ('DI2', 'Borrar Línea\nEje Y'), ('DI3', 'Cambiar Área\nde Superficie'),
            ('DI4', 'Enviar\nDatos'), ('DI5', 'Precisión'),
            ('DI6', 'Enviar\nDatos'), ('DI7', 'Cambiar\nEsquina'),
            ('DI8', 'Línea de Ayuda\nEje Y'), ('DI9', 'Línea de Ayuda\nEje X'),
            ('DI10', 'Añadir Línea\nEje Y'), ('DI11', 'Borrar Línea\nEje X'),
            ('DI12', 'Añadir Línea\nEje X')
        ]

        for i, (key, name) in enumerate(button_names):
            button = QPushButton(name)
            button.setCheckable(True)
            button.clicked.connect(lambda checked, k=key: self.toggle_button(k, checked))
            self.update_button_style(button, 'False')
            self.buttons[key] = button
            # Colocar botón en la cuadrícula: calcular fila y columna
            row = 2 + i // 6
            col = i % 6
            grid_layout.addWidget(button, row, col)

            # Conectar botones al método emit_data_changed
            button.clicked.connect(self.emit_data_changed1)

        # Selector para activar/desactivar la conexión serial
        self.serial_switch = QCheckBox("Activar Conexión Serial")
        self.serial_switch.setChecked(False)
        self.serial_switch.toggled.connect(self.toggle_serial_connection)
        grid_layout.addWidget(self.serial_switch, row + 1, 0, 1, 6)  # Abarcar todas las columnas utilizadas para botones

    def toggle_serial_connection(self, checked):
        if checked:
            try:
                self.ser_thread = SerialThread("COM4")
                self.ser_thread.data_received.connect(self.update_data)
                self.ser_thread.start()
                print("Conexión serial activada.")
            except Exception as e:
                print(f"Error al abrir el puerto serial: {e}")
                self.serial_switch.setChecked(False)
        else:
            if self.ser_thread:
                self.ser_thread.stop()
                self.ser_thread = None
            print("Conexión serial desactivada.")

    def toggle_button(self, key, checked):
        button = self.buttons[key]
        self.update_button_style(button, 'True' if checked else 'False')

    def update_button_style(self, button, value):
        if value == 'True':
            button.setStyleSheet("background-color: green; color: white;")
            button.setText(f"{button.text().split(':')[0]}: Activado")
        else:
            button.setStyleSheet("background-color: red; color: white;")
            button.setText(f"{button.text().split(':')[0]}")

    def update_data(self, data):
        print("Datos recibidos:", data)
        sensors = data.split(',')
        for sensor in sensors:
            try:
                key, value = sensor.strip().split(':')
                if key.startswith('Pot') and key in self.sliders:
                    self.sliders[key].setValue(int(value))
                elif key in self.buttons:
                    self.update_button_style(self.buttons[key], 'True' if value == '0' else 'False')
            except ValueError:
                print(f"Error en el formato de datos recibidos: '{sensor}'")
                continue
            except KeyError:
                print(f"KeyError con clave '{key}'. Posible clave mal formateada o no definida.")
                continue

    def emit_data_changed1(self):
        global datos_botonera_sliders
        # Emitir la señal data_changed con el diccionario de datos actualizado
        data = self.get_data()
        datos_botonera_sliders.update(data)
        print(f"Emit data_changed: {datos_botonera_sliders}")  # Log to check the data being emitted
        # self.data_changed1.emit()

    def get_data(self):
        data = {}
        # Obtener valores de los sliders
        data['Pot1'] = self.sliders['Pot1'].value()
        data['Pot2'] = self.sliders['Pot2'].value()
        # Obtener estado de los botones
        for key, button in self.buttons.items():
            data[key] = button.isChecked()
        return data

    def closeEvent(self, event):
        if self.ser_thread:
            self.ser_thread.stop()
        super().closeEvent(event)


#############################################################################################

class CustomWidget(QWidget):
    data_changed = pyqtSignal(dict)
    def __init__(self):
        super().__init__()
        
        # Crear el layout grid para organizar los elementos
        self.layout = QGridLayout()

        # Crear el label para mostrar los frames
        self.label = QLabel("Frames")
        self.layout.addWidget(self.label, 0, 0, 3, 1)  # (fila, columna, rowspan, colspan)

        # Crear botón
        self.button = QPushButton("Botón")
        self.layout.addWidget(self.button, 0, 1)

        # Crear los sliders
        self.slider1 = QSlider(Qt.Orientation.Horizontal)
        self.slider2 = QSlider(Qt.Orientation.Horizontal)
        self.layout.addWidget(self.slider1, 1, 1)
        self.layout.addWidget(self.slider2, 2, 1)

        # Establecer el layout principal del widget
        self.setLayout(self.layout)
        self.slider1.valueChanged.connect(self.emit_data_changed)
        self.slider2.valueChanged.connect(self.emit_data_changed)

        # Conectar la señal de clic del botón al método emit_data_changed
        self.button.clicked.connect(self.emit_data_changed)

    def emit_data_changed(self):
        global datos_botonera_sliders
        # Emitir la señal data_changed con el diccionario de datos actualizado
        data = self.get_data()
        datos_botonera_sliders.update(data)
        print(f"Emit data_changed: {datos_botonera_sliders}")  # Log to check the data being emitted
        #self.data_changed.emit()

    def get_data(self):
            return {
                "Brillo": self.slider1.value(),
                "Contraste": self.slider2.value(),

            }

class Process_proyecciones(multiprocessing.Process):
    def __init__(self, matplotlib_iniciado, parametros_vectores,flag_creacion_3D,imagen_proyeccion):
        super().__init__()
        self.imagen_proyeccion = imagen_proyeccion
        self.flag_creacion_3D = flag_creacion_3D
        self.matplotlib_iniciado = matplotlib_iniciado
        self.parametros_vectores = parametros_vectores

    def run(self):
        if not self.imagen_proyeccion.empty():
            frame = self.imagen_proyeccion.get()

        if not self.parametros_vectores.empty():
            dic_parametros = self.parametros_vectores.get()
            print(dic_parametros)
            if "tipo" in dic_parametros:
                tipo_datos = dic_parametros["tipo"]
                if tipo_datos == "parametros_vectores":
                    if "rvecs_1" in dic_parametros and "tvecs_1" in dic_parametros:
                        rvecs = dic_parametros["rvecs_1"]
                        tvecs = dic_parametros["tvecs_1"]
                        corners_reales_1 = dic_parametros["corners_reales_1"]
                        rvecs_normalized = np.array(rvecs) / np.linalg.norm(rvecs)
                        tvecs_normalized = np.array(tvecs) / np.linalg.norm(tvecs)
                        rot_matrix, _ = cv2.Rodrigues(rvecs)
                        vertices = np.dot(vertices, rot_matrix.T)
                elif tipo_datos == "otro_diccionario":
                    print("se recibieron distancias")
                    distancia_camara_superficie = dic_parametros["distancia_camara_superficie"]
                    distancia_proyector_superficie = dic_parametros["distancia_proyector_superficie"]
                    distancia_camara_proyector = dic_parametros["distancia_camara_proyector"]
                    print("Distancia cámara-superficie:", distancia_camara_superficie)
                    print("Distancia proyector-superficie:", distancia_proyector_superficie)
                    print("Distancia cámara-proyector:", distancia_camara_proyector)

        def cerrar(event):
            self.flag_creacion_3D = False
            self.matplotlib_iniciado.value = False
#--------------------------------------------------------------------------------------------------------------
class ProjectionWindow(QWidget):
    def __init__(self, get_frame):
        super().__init__()
        self.setWindowTitle('Cambiar entre Bordes y Sin Bordes')

        self.button_toggle = QPushButton('Cambiar Modo', self)
        self.button_toggle.clicked.connect(self.toggle_border_mode)

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.button_toggle)
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.with_border = True
        self.get_frame = get_frame
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(50)  # Actualiza cada 100 milisegundos

        self.update_frame()

    def toggle_border_mode(self):
        self.with_border = not self.with_border
        if self.with_border:
            self.setWindowFlag(Qt.WindowType.FramelessWindowHint, False)
        else:
            self.setWindowFlag(Qt.WindowType.FramelessWindowHint, True)
        self.show()

    def update_frame(self):
        frame = self.get_frame()
        if frame is not None and frame.size != 0:
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            qimg = QImage(frame.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(qimg))
    
    def closeEvent(self, event):
        self.timer.stop()


#--------------------------------------------------------------------------------------------------------------

class Ventana_Principal(QMainWindow):
    
    def __init__(self):
        super().__init__()
        try:
            
            self.Iniciar_variables_ventana_principal()
            self.inicializarUI()
            self.shared_frame_queue = Queue()  # Crear la cola compartida
            self.barra_de_estado = QStatusBar()
            self.setStatusBar(self.barra_de_estado)
        except Exception as e:
            print(f"Excepción en el hilo de ejecución 4: {e}")
    
    def Iniciar_variables_ventana_principal(self):
        
        self.input_queue_ROI1 = multiprocessing.Queue(maxsize= 5)
        self.input_queue_ROI2 = multiprocessing.Queue(maxsize= 5)
        self.input_queue_ROI3 = multiprocessing.Queue(maxsize= 5)
        self.input_queue_ROI4 = multiprocessing.Queue(maxsize= 5)
        self.comunicate = multiprocessing.Queue(maxsize= 2)
        self.matplotlib_iniciado = multiprocessing.Value('i', False)
        self.cambio_color_queue = multiprocessing.Queue(maxsize = 5)
        self.parametros_vectores = multiprocessing.Queue(maxsize = 5)
        self.imagen_proyeccion = multiprocessing.Queue(maxsize = 5)
        self.dic_thread = DICThread()
        self.video_thread = VideoStreamThread(self.input_queue_ROI1,self.input_queue_ROI2,self.input_queue_ROI3,self.input_queue_ROI4,self.imagen_proyeccion)
        ###########-----------------------------------------------------------------------------------------
        #estos parametros cambian dependidendo de la camara que se use
            
#generacion de UI Principal-----------------------------------------
    def inicializarUI(self):
        self.setGeometry(250,100,1250,750)
        self.setWindowTitle("Interfaz_v9.2") 
        self.generate_main_window()
        self.created_actions()
        self.show()
#aqui se colocan todas las demas ventanas
    def generate_main_window(self):
        self.create_menu()
        self.create_dock_modificacion_de_datos() 
        self.create_dock_2()
        self.create_ventana_central()
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
        self.dock1.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
        self.contenedor_de_widgets = QWidget()
        self.main_box_dock1 = QGridLayout()
        text1 = QLabel("Distancias entre marcas")
        text1.setFixedHeight(20)
        text1.setStyleSheet("background-color: #dadada")
        self.main_box_dock1.addWidget(text1, 1, 0, 1, 2)
        # Ingreso de datos-----------------------------------------------------------------
        cm_ancho_entre_puntos_label = QLabel('cm_ancho_entre_puntos:')
        cm_ancho_entre_puntos_lineedit = QLineEdit()
        cm_alto_entre_puntos_label = QLabel('cm_alto_entre_puntos:')
        cm_alto_entre_puntos_lineedit = QLineEdit()

        # Agregamos los widgets al main_box_dock1
        self.main_box_dock1.addWidget(cm_ancho_entre_puntos_label, 2, 0)
        self.main_box_dock1.addWidget(cm_ancho_entre_puntos_lineedit, 2, 1)
        self.main_box_dock1.addWidget(cm_alto_entre_puntos_label, 3, 0)
        self.main_box_dock1.addWidget(cm_alto_entre_puntos_lineedit, 3, 1)


        self.text2 = QLabel("creacion de modelado 3D")
        self.text2.setFixedHeight(20)
        self.text2.setStyleSheet("background-color: #dadada")
        self.main_box_dock1.addWidget(self.text2, 4, 0,1,2)

        self.btn_cambiar_color = QPushButton("Cambiar Color")

        self.main_box_dock1.addWidget(self.btn_cambiar_color, 6, 1,1,1)
        self.text3 = QLabel("distancias")
        self.text3.setFixedHeight(20)
        self.text3.setStyleSheet("background-color: #dadada")
        self.main_box_dock1.addWidget(self.text3, 7, 0,1,2)
        dist_camara_superficie_label = QLabel('Distancia (cámara-superficie):')
        self.dist_camara_superficie_lineedit = QLineEdit()
        dist_proyector_superficie_label = QLabel('Distancia (proyector-superficie):')
        self.dist_proyector_superficie_lineedit = QLineEdit()
        dist_camara_proyector_label = QLabel('Distancia (cámara-proyector):')
        self.dist_camara_proyector_lineedit = QLineEdit()
        boton_inreso_distancias = QPushButton("Calcular")

        # Agregamos los widgets al main_box_dock1
        self.main_box_dock1.addWidget(dist_camara_superficie_label, 8, 0)
        self.main_box_dock1.addWidget(self.dist_camara_superficie_lineedit, 8, 1)
        self.main_box_dock1.addWidget(dist_proyector_superficie_label, 9, 0)
        self.main_box_dock1.addWidget(self.dist_proyector_superficie_lineedit, 9, 1)
        self.main_box_dock1.addWidget(dist_camara_proyector_label, 10, 0)
        self.main_box_dock1.addWidget(self.dist_camara_proyector_lineedit, 10, 1)
        self.main_box_dock1.addWidget(boton_inreso_distancias, 11, 0,1,2)
        self.main_box_dock1.setRowStretch(12,1)
        self.dic_thread.start()
        self.contenedor_de_widgets.setLayout(self.main_box_dock1)
        self.dock1.setWidget(self.contenedor_de_widgets)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea,self.dock1)
        boton_inreso_distancias.clicked.connect(self.calcular_distancias)
    
    def calcular_distancias(self):
        # Obtenemos los valores de los LineEdit
        global distancia_camara_proyector,distancia_camara_superficie,distancia_proyector_superficie
        try:
            resultado = {
                            "distancia_camara_superficie": float(self.dist_camara_superficie_lineedit.text()),
                            "distancia_proyector_superficie": float(self.dist_proyector_superficie_lineedit.text()),
                            "distancia_camara_proyector": float(self.dist_camara_proyector_lineedit.text()),
                            "tipo":"otro_diccionario"
                        }
            self.parametros_vectores.put(resultado)
            print("se envio distancias")
        except ValueError:
            print("Error: uno o más valores ingresados no son números válidos.")
        

    
    def actualizar_cm_entre_puntos(self):
        global cm_alto_entre_puntos,cm_ancho_entre_puntos
        cm_ancho_entre_puntos = float(self.main_box_dock1.itemAtPosition(2, 1).widget().text())
        cm_alto_entre_puntos = float(self.main_box_dock1.itemAtPosition(3, 1).widget().text())
        print("cm_ancho_entre_puntos:", str(cm_ancho_entre_puntos))
        print("cm_alto_entre_puntos:", str(cm_alto_entre_puntos))
        
    def create_ventana_central(self):
        
        tab_bar = QTabWidget(self)
        self.contenedor1 = QWidget()
        ventana_video_principal = MiVentana(self.video_thread,self.dic_thread,self.midockwidget)
        tab_bar.addTab(ventana_video_principal,"contenedor1")
        self.contenedor2 = QWidget()
        tab_bar.addTab(self.contenedor2,"contenedor2")
        main_container = QWidget()
        open_projection_button = QPushButton("Abrir ventana de proyección")
        open_projection_button.clicked.connect(self.open_projection_window)
        central_layout = QVBoxLayout()
        self.textbotonera = QLabel("Botonera")
        self.textbotonera.setFixedHeight(20)
        self.textbotonera.setStyleSheet("background-color: #dadada")
        central_layout.addWidget(self.textbotonera)
        self.serialwidget = SerialControlWidget()
        central_layout.addWidget(self.serialwidget)
        self.textpestaña2 = QLabel("Imagen de proyeccion")
        self.textpestaña2.setFixedHeight(20)
        self.textpestaña2.setStyleSheet("background-color: #dadada")
        central_layout.addWidget(self.textpestaña2)
        self.btn_imagen_proyeccion = QPushButton("Iniciar_Process_proyecciones")
        
        self.btn_imagen_proyeccion.clicked.connect(lambda: self.iniciar_Process_proyecciones(self.matplotlib_iniciado,self.parametros_vectores,self.imagen_proyeccion))
        central_layout.addWidget(self.btn_imagen_proyeccion)
        
        self.CustomWidget = CustomWidget()
        central_layout.addWidget(self.CustomWidget)



        self.textpestaña = QLabel("Ventana de proyeccion")
        self.textpestaña.setFixedHeight(20)
        self.textpestaña.setStyleSheet("background-color: #dadada")
        central_layout.addWidget(self.textpestaña)
        central_layout.addWidget(open_projection_button)
        
        
        






        central_layout.addStretch(1)
        self.contenedor2.setLayout(central_layout)
        tab_h_box = QHBoxLayout()
        tab_h_box.addWidget(tab_bar)
        main_container.setLayout(tab_h_box)
        self.setCentralWidget(main_container)

        
    def iniciar_Process_proyecciones(self,matplotlib_iniciado,parametros_vectores,imagen_proyeccion):
        try:
            global flag_creacion_3D
            if not matplotlib_iniciado.value:
                #flag_creacion_3D = True
                matplotlib_process = Process_proyecciones(matplotlib_iniciado,parametros_vectores,flag_creacion_3D,imagen_proyeccion)
                matplotlib_process.start()
                matplotlib_iniciado.value = True
        except Exception as e:
            print(f"Excepción INICIAR MATPLOTLIB: {e}")

    def open_projection_window(self):
        self.projection_window = ProjectionWindow(self.video_thread.get_latest_frame)
        # Obtén la lista de todas las pantallas disponibles
        screens = QGuiApplication.screens()
        if len(screens) > 1:
            # Selecciona la segunda pantalla
            second_screen = screens[1]
            self.projection_window.setGeometry(second_screen.geometry())
        self.projection_window.show()

    def create_dock_2(self):
        self.midockwidget = MiDockWidget(self.video_thread,self.dic_thread,self.input_queue_ROI1,self.input_queue_ROI2,self.input_queue_ROI3,self.input_queue_ROI4,self.parametros_vectores)
        self.dock2 = QDockWidget()
        self.dock2.setWidget(self.midockwidget)

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

    def closeEvent(self, event):
        print("Inicio Close Event --------------------------------------------")
        try: 
            print("Finalizacion treads")
            self.stop_threads()
            
            print("Final del código------------------------------------------------")
        except Exception as e:
            print(f"Excepción en stop_threads: {e}")

    def stop_threads(self):
        print("Inicio stop tread")
        self.midockwidget.image_processor_thread.finalizar_process()
        
        print("Se finalizo process")
        if self.midockwidget.image_processor_thread is not None and self.midockwidget.image_processor_thread.isRunning():
            self.midockwidget.image_processor_thread.requestInterruption()
            self.midockwidget.image_processor_thread.quit()
            self.midockwidget.image_processor_thread.wait()
            
            print("Se finalizo image processor tread")
        else:
            print("El image processor no esta activo")
        
        if self.video_thread is not None and self.video_thread.isRunning():
            self.video_thread.capturando = False
            self.video_thread.quit()
            self.video_thread.wait()
            print("Se finalizo video tread")
        else:
            print("El video tread no esta activo")



if __name__ == '__main__':
    print("SE INICIO EL CODIO")
    cm_ancho_entre_puntos = None
    cm_alto_entre_puntos = None
    cords_ROI_1 = None
    cords_ROI_2 = None
    cords_ROI_3 = None
    cords_ROI_4 = None
    XYZ_Calculados_P1 = None  
    XYZ_Calculados_P2 = None 
    XYZ_Calculados_P3 = None
    XYZ_Calculados_P4 = None
    flag_creacion_3D = False
    distancia_camara_superficie = None
    distancia_proyector_superficie = None
    distancia_camara_proyector = None
    Dictvect = {}
    datos_botonera_sliders = {}
    calibration_factor = 0.7283353225169037
    camera_matrix = np.array([[695.41363501, 0, 316.72866174],
                              [0, 690.8243246, 238.12973815],
                              [0, 0, 1]])
    distortion_parameters = np.array([[0.2147207, -1.43701464, -0.00359401, 0.00228601, 1.99576813]])
    # Obtiene la información de la CPU
    app = QApplication(sys.argv)
    ventana = Ventana_Principal()
    sys.exit(app.exec())
