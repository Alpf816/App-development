import multiprocessing
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
                            QSizePolicy,
                            QHeaderView,
                            QSpacerItem)
from PyQt6.QtGui import QImage, QPixmap,QAction,QKeySequence,QIntValidator
from PyQt6.QtCore import Qt,QThread, pyqtSignal, QMutex, QMutexLocker,QTimer,QObject, pyqtSlot,QCoreApplication,QTimer
import cv2
import numpy as np
import time
from queue import Queue

width_video_capture = int
height_video_capture = int



class VideoStreamThread(QThread):
    frame_actualizado = pyqtSignal(QImage)
    finalizado = pyqtSignal()
    frame_captured = pyqtSignal(np.ndarray)
    
    
    def __init__(self,input_queue_ROI1,input_queue_ROI2,input_queue_ROI3,input_queue_ROI4):
        super().__init__()
        
        self.capturando = False
        self.pausado = False
        self.latest_frame = None
        self.frame_lock = QMutex()

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
            
    def get_latest_frame(self):
        with QMutexLocker(self.frame_lock):
            return self.latest_frame if self.latest_frame is not None else None

    def run(self):
        try:
            coordinate_image_initialized = False
            coordinate_image = None
            Yatengodatos = True
            self.capturando = True
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
                
                #inicio_iteracion = time.time()
                #print("Antes de capturar el fotograma")
                ret, frame = video_stream.read()

                if not ret:
                    raise Exception(f"Error al capturar el fotograma: {video_stream.get(cv2.CAP_PROP_FRAME_WIDTH)} x {video_stream.get(cv2.CAP_PROP_FRAME_HEIGHT)}")

                with QMutexLocker(self.frame_lock):
                    self.latest_frame = frame
                    #print("frame copiado y enviado")

                
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
                global cords_ROI_1,cords_ROI_2, cords_ROI_3, cords_ROI_4

                if cords_ROI_1 is not None and cords_ROI_2 is not None and cords_ROI_3 is not None and cords_ROI_4  is not None:
                    print(cords_ROI_1,cords_ROI_2, cords_ROI_3, cords_ROI_4)
                    rect_coords = np.array([cords_ROI_1, cords_ROI_3, cords_ROI_4,cords_ROI_2] , dtype=np.int32)
                    cv2.polylines(self.frame_video_ventanacentral, [rect_coords], isClosed=True, color=(0, 0, 255), thickness=2)
                    #cv2.line(self.frame_video_ventanacentral, cords_ROI_1, cords_ROI_2, (255, 0, 0), 2)
                    #cv2.line(self.frame_video_ventanacentral, cords_ROI_2, cords_ROI_4, (255, 0, 0), 2)
                    #cv2.line(self.frame_video_ventanacentral, cords_ROI_3, cords_ROI_1, (255, 0, 0), 2)
                    #cv2.line(self.frame_video_ventanacentral, cords_ROI_4, cords_ROI_3, (255, 0, 0), 2) 

                

                combined_image = self.overlay_images(self.frame_video_ventanacentral, coordinate_image)

                q_image = QImage(combined_image.data, width_video_capture, height_video_capture, width_video_capture * 3, QImage.Format.Format_RGB888)
                self.frame_actualizado.emit(q_image)
                QThread.msleep(20)
                #fin_iteracion = time.time()
                

            QThread.msleep(20)
            #duracion_iteracion = fin_iteracion - inicio_iteracion
            #tasa_de_fps_aprox = 1/duracion_iteracion
            #print(f'tasa de fps aprox: {tasa_de_fps_aprox} fps')

        except Exception as e:
            print(f"Excepción en el hilo de ejecución: {e}")
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
            print(f"Excepción en el hilo de ejecución: {e}")

    def actualizar_frame(self, q_image):
        try:    
            if q_image:
                pixmap = QPixmap.fromImage(q_image)
                margin = self.table_widget.width()
                pixmap = pixmap.scaledToWidth(margin-10)
                self.label_video.setPixmap(pixmap)
        except Exception as e:
            print(f"Excepción en el hilo de ejecución: {e}")
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
    def __init__(self, video_thread,dic_thread,input_queue_ROI1,input_queue_ROI2,input_queue_ROI3,input_queue_ROI4):
        super().__init__()
        self.input_queue_ROI1 = input_queue_ROI1
        self.input_queue_ROI2 = input_queue_ROI2
        self.input_queue_ROI3 = input_queue_ROI3
        self.input_queue_ROI4 = input_queue_ROI4
        self.dic_thread = dic_thread
        self.hilo_video = video_thread
        self.presets_combobox = QComboBox(self)
        self.presets_combobox.addItems(["Original", "Seleccion de colores", "Contornos"])
        self.presets_combobox.currentIndexChanged.connect(self.on_preset_changed)
        # Crear instancia de ImageProcessorThread y pasarla a MiDockWidget
        self.image_processor_thread = ImageProcessorThread(self.hilo_video.get_latest_frame,self.dic_thread,self.input_queue_ROI1,self.input_queue_ROI2,self.input_queue_ROI3,self.input_queue_ROI4,self.hilo_video)
        
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

class ImageProcessorThread(QThread):
    processed_frame_signal = pyqtSignal(QImage)
    processed_frame_signal1 = pyqtSignal(QImage)
    processed_frame_signal2 = pyqtSignal(QImage)
    processed_frame_signal3 = pyqtSignal(QImage)
    pausar_signal = pyqtSignal()
    reanudar_signal = pyqtSignal()
    diccionario_del_IPT = dict
    TonMin1 = 0
    TonMax1 = 0
    PurMin1 = 0
    PurMax1 = 0
    LumMin1 = 0
    LumMax1 = 0
    KerX1 = 0
    KerY1 = 0
    TonMin2 = 0
    TonMax2 = 0
    PurMin2 = 0
    PurMax2 = 0
    LumMin2 = 0
    LumMax2 = 0
    KerX2 = 0
    KerY2 = 0
    TonMin3 = 0
    TonMax3 = 0
    PurMin3 = 0
    PurMax3 = 0
    LumMin3 = 0
    LumMax3 = 0
    KerX3 = 0
    KerY3 = 0
    TonMin4 = 0
    TonMax4 = 0
    PurMin4 = 0
    PurMax4 = 0
    LumMin4 = 0
    LumMax4 = 0
    KerX4 = 0
    KerY4 = 0
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

    
    def __init__(self, get_frame_function, dic_thread,input_queue_ROI1,input_queue_ROI2,input_queue_ROI3,input_queue_ROI4,hilo_video):
        super().__init__()
        self.input_queue_ROI1 = input_queue_ROI1
        self.input_queue_ROI2 = input_queue_ROI2
        self.input_queue_ROI3 = input_queue_ROI3
        self.input_queue_ROI4 = input_queue_ROI4
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
        self.process_1 = VideoProcess(self.input_queue_ROI1,self.output_queue_ROI1,self.DIC_Queue_ROI_1,self.DIC_Result_queue_ROI1,1)
        self.Bucle_frames_processados_1 = VideoProcessingThread(self.output_queue_ROI1,self.processed_frame_signal,self.DIC_Result_queue_ROI1,1)
        self.process_2 = VideoProcess(self.input_queue_ROI2,self.output_queue_ROI2,self.DIC_Queue_ROI_2,self.DIC_Result_queue_ROI2,2)
        self.Bucle_frames_processados_2 = VideoProcessingThread(self.output_queue_ROI2,self.processed_frame_signal1,self.DIC_Result_queue_ROI2,2)
        self.process_3 = VideoProcess(self.input_queue_ROI3,self.output_queue_ROI3,self.DIC_Queue_ROI_3,self.DIC_Result_queue_ROI3,3)
        self.Bucle_frames_processados_3 = VideoProcessingThread(self.output_queue_ROI3,self.processed_frame_signal2,self.DIC_Result_queue_ROI3,3)
        self.process_4 = VideoProcess(self.input_queue_ROI4,self.output_queue_ROI4,self.DIC_Queue_ROI_4,self.DIC_Result_queue_ROI4,4)
        self.Bucle_frames_processados_4 = VideoProcessingThread(self.output_queue_ROI4,self.processed_frame_signal3,self.DIC_Result_queue_ROI4,4)




        
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
                    
                    time.sleep(1)

                elif self.current_preset == "Contornos":
                    #print("se Inicio Contornos")
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

        self.TonMin1 = self.diccionario_del_IPT.get("Tonalidad Minima S1")
        self.TonMax1 = self.diccionario_del_IPT.get("Tonalidad Maxima S1")
        self.PurMin1 = self.diccionario_del_IPT.get("Pureza Minima S1")
        self.PurMax1 = self.diccionario_del_IPT.get("Pureza Maxima S1")
        self.LumMin1 = self.diccionario_del_IPT.get("Luminosidad Minima S1")
        self.LumMax1 = self.diccionario_del_IPT.get("Luminosidad Maxima S1")
        self.KerX1 = self.diccionario_del_IPT.get("Kernel X S1")
        self.KerY1 = self.diccionario_del_IPT.get("Kernel Y S1")
        self.O_ROI_1X = self.diccionario_del_IPT.get("Origen de ROI color 1 X")
        self.O_ROI_1Y = self.diccionario_del_IPT.get("Origen de ROI color 1 Y")
        self.WH_ROI_1X = self.diccionario_del_IPT.get("width_height ROI color 1 X")
        self.WH_ROI_1Y = self.diccionario_del_IPT.get("width_height ROI color 1 Y")


        self.TonMin2 = self.diccionario_del_IPT.get("Tonalidad Minima S2")
        self.TonMax2 = self.diccionario_del_IPT.get("Tonalidad Maxima S2")
        self.PurMin2 = self.diccionario_del_IPT.get("Pureza Minima S2")
        self.PurMax2 = self.diccionario_del_IPT.get("Pureza Maxima S2")
        self.LumMin2 = self.diccionario_del_IPT.get("Luminosidad Minima S2")
        self.LumMax2 = self.diccionario_del_IPT.get("Luminosidad Maxima S2")
        self.KerX2 = self.diccionario_del_IPT.get("Kernel X S2")
        self.KerY2 = self.diccionario_del_IPT.get("Kernel Y S2")
        self.O_ROI_2X = self.diccionario_del_IPT.get("Origen de ROI color 2 X")
        self.O_ROI_2Y = self.diccionario_del_IPT.get("Origen de ROI color 2 Y")
        self.WH_ROI_2X = self.diccionario_del_IPT.get("width_height ROI color 2 X")
        self.WH_ROI_2Y = self.diccionario_del_IPT.get("width_height ROI color 2 Y")


        self.TonMin3 = self.diccionario_del_IPT.get("Tonalidad Minima S3")
        self.TonMax3 = self.diccionario_del_IPT.get("Tonalidad Maxima S3")
        self.PurMin3 = self.diccionario_del_IPT.get("Pureza Minima S3")
        self.PurMax3 = self.diccionario_del_IPT.get("Pureza Maxima S3")
        self.LumMin3 = self.diccionario_del_IPT.get("Luminosidad Minima S3")
        self.LumMax3 = self.diccionario_del_IPT.get("Luminosidad Maxima S3")
        self.KerX3 = self.diccionario_del_IPT.get("Kernel X S3")
        self.KerY3 = self.diccionario_del_IPT.get("Kernel Y S3")
        self.O_ROI_3X = self.diccionario_del_IPT.get("Origen de ROI color 3 X")
        self.O_ROI_3Y = self.diccionario_del_IPT.get("Origen de ROI color 3 Y")
        self.WH_ROI_3X = self.diccionario_del_IPT.get("width_height ROI color 3 X")
        self.WH_ROI_3Y = self.diccionario_del_IPT.get("width_height ROI color 3 Y")


        self.TonMin4 = self.diccionario_del_IPT.get("Tonalidad Minima S4")
        self.TonMax4 = self.diccionario_del_IPT.get("Tonalidad Maxima S4")
        self.PurMin4 = self.diccionario_del_IPT.get("Pureza Minima S4")
        self.PurMax4 = self.diccionario_del_IPT.get("Pureza Maxima S4")
        self.LumMin4 = self.diccionario_del_IPT.get("Luminosidad Minima S4")
        self.LumMax4 = self.diccionario_del_IPT.get("Luminosidad Maxima S4")
        self.KerX4 = self.diccionario_del_IPT.get("Kernel X S4")
        self.KerY4 = self.diccionario_del_IPT.get("Kernel Y S4")
        self.O_ROI_4X = self.diccionario_del_IPT.get("Origen de ROI color 4 X")
        self.O_ROI_4Y = self.diccionario_del_IPT.get("Origen de ROI color 4 Y")
        self.WH_ROI_4X = self.diccionario_del_IPT.get("width_height ROI color 4 X")
        self.WH_ROI_4Y = self.diccionario_del_IPT.get("width_height ROI color 4 Y")

        if all(v != 0 for v in [self.WH_ROI_1X,self.WH_ROI_1Y]):
            self.diccionario_ROI_1 = {
            'TonMin': self.TonMin1,
            'TonMax': self.TonMax1,
            'PurMin': self.PurMin1,
            'PurMax': self.PurMax1,
            'LumMin': self.LumMin1,
            'LumMax': self.LumMax1,
            'KerX': self.KerX1,
            'KerY': self.KerY1,
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
                'TonMin': self.TonMin2,
                'TonMax': self.TonMax2,
                'PurMin': self.PurMin2,
                'PurMax': self.PurMax2,
                'LumMin': self.LumMin2,
                'LumMax': self.LumMax2,
                'KerX': self.KerX2,
                'KerY': self.KerY2,
                'O_ROI_X': self.O_ROI_2X,
                'O_ROI_Y': self.O_ROI_2Y,
                'WH_ROI_X': self.WH_ROI_2X,
                'WH_ROI_Y': self.WH_ROI_2Y,
            }  
            if not self.DIC_Queue_ROI_2.full():
                self.DIC_Queue_ROI_2.put(self.diccionario_ROI_2)

        if all(v != 0 for v in [self.WH_ROI_3X, self.WH_ROI_3Y]):
            self.diccionario_ROI_3 = {
                'TonMin': self.TonMin3,
                'TonMax': self.TonMax3,
                'PurMin': self.PurMin3,
                'PurMax': self.PurMax3,
                'LumMin': self.LumMin3,
                'LumMax': self.LumMax3,
                'KerX': self.KerX3,
                'KerY': self.KerY3,
                'O_ROI_X': self.O_ROI_3X,
                'O_ROI_Y': self.O_ROI_3Y,
                'WH_ROI_X': self.WH_ROI_3X,
                'WH_ROI_Y': self.WH_ROI_3Y,
            }  
            if not self.DIC_Queue_ROI_3.full():
                self.DIC_Queue_ROI_3.put(self.diccionario_ROI_3)

        if all(v != 0 for v in [self.WH_ROI_4X, self.WH_ROI_4Y]):
            self.diccionario_ROI_4 = {
                'TonMin': self.TonMin4,
                'TonMax': self.TonMax4,
                'PurMin': self.PurMin4,
                'PurMax': self.PurMax4,
                'LumMin': self.LumMin4,
                'LumMax': self.LumMax4,
                'KerX': self.KerX4,
                'KerY': self.KerY4,
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
    def __init__(self,input_queue_ROI,output_queue_ROI,DIC_Queue,DIC_Result_queue_ROI,int_valor_process):
                
        super().__init__()
        self.input_queue = input_queue_ROI
        self.output_queue = output_queue_ROI
        self.DIC_Queue = DIC_Queue
        self.DIC_Result_queue_ROI = DIC_Result_queue_ROI
        self.int_valor_process = int_valor_process
        self.O_ROI_H = 0
        self.O_ROI_V = 0
        self.W_ROI = 0
        self.H_ROI = 0
        self.TonMin = 0
        self.TonMax = 0
        self.PurMin = 0
        self.PurMax = 0
        self.LumMin = 0 
        self.LumMax = 0
        self.KerX = 0
        self.KerY = 0
        self.O_ROI_X = 0
        self.O_ROI_Y = 0
        self.WH_ROI_X = 0
        self.WH_ROI_Y = 0

        
        self.process_flag_interno = True
        print("Init Videoprocess")

    def run(self):
        print("process iniciado")
        try:
            while self.process_flag_interno:
                if not self.DIC_Queue.empty():
                    self.ROI_DIC = self.DIC_Queue.get()
                   
                    if isinstance(self.ROI_DIC, dict):
                        self.TonMin = self.ROI_DIC.get('TonMin')
                        self.TonMax = self.ROI_DIC.get('TonMax')
                        self.PurMin = self.ROI_DIC.get('PurMin')
                        self.PurMax = self.ROI_DIC.get('PurMax')
                        self.LumMin = self.ROI_DIC.get('LumMin')
                        self.LumMax = self.ROI_DIC.get('LumMax')
                        self.KerX = self.ROI_DIC.get('KerX')
                        self.KerY = self.ROI_DIC.get('KerY')
                        self.O_ROI_X = self.ROI_DIC.get('O_ROI_X')
                        self.O_ROI_Y = self.ROI_DIC.get('O_ROI_Y')
                        self.WH_ROI_X = self.ROI_DIC.get('WH_ROI_X')
                        self.WH_ROI_Y = self.ROI_DIC.get('WH_ROI_Y')
                        #print(self.ROI_DIC)
                    else:
                        print("Se envio el dict pero no lo contiene los datos")

                if not self.input_queue.empty() and all(v != 0 for v in [self.WH_ROI_X,self.WH_ROI_Y]):
                    frame = self.input_queue.get()
                    
                    hsv1 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                    color_oscuro1 = np.array([self.TonMin, self.PurMin, self.LumMin])
                    color_claro1 = np.array([self.TonMax, self.PurMax, self.LumMax])
                    mascara1 = cv2.inRange(hsv1, color_oscuro1, color_claro1)

                    contorno1, _ = cv2.findContours(mascara1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    contour_image1 = np.zeros((frame.shape[0], frame.shape[1], 3), dtype=np.uint8)

                    # Detección del centro del círculo y dibujo solo los círculos completamente llenos
                    for contorno in contorno1:
                        if 20 < len(contorno) < 250:
                            # Calcular el área del contorno y del círculo encerrado por el límite convexo
                            area_contorno = cv2.contourArea(contorno)
                            hull = cv2.convexHull(contorno)
                            area_hull = cv2.contourArea(hull)

                            # Calcular el porcentaje de llenado
                            porcentaje_llenado = (area_contorno / area_hull) * 100

                            # Filtrar círculos con al menos el porcentaje requerido de llenado
                            if porcentaje_llenado >= 90:
                                (x, y), radio = cv2.minEnclosingCircle(contorno)
                                centro = (int(x), int(y))
                                self.centro_verdadero = (int(x) + int(self.O_ROI_X),int(y) +int(self.O_ROI_Y))
                                if self.centro_verdadero is not None:
                                    self.DIC_Result_queue_ROI.put(self.centro_verdadero)
                                radio = int(radio)
                                cv2.circle(frame, centro, radio, (0, 255, 0), 2)
                                # Mostrar las coordenadas del centro en el frame
                                texto = f"Centro: ({centro[0]+ self.O_ROI_X}, {centro[1]+self.O_ROI_Y})"
                                cv2.putText(frame, texto, (centro[0] - 50, centro[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    if contour_image1 is not None and contour_image1.shape[0] > 0 and contour_image1.shape[1] > 0:
                        self.output_queue.put(frame)
                        
                    time.sleep(0.02)
                else:
                    time.sleep(0.02)
            else:
                    time.sleep(0.01)
        except Exception as e:
            print(f"Excepción en el process {self.int_valor_process}: {e}")
        print("Se Finalizo el process")
           
    def finalizar_process_interno(self):
        self.process_flag_interno = False

class VideoProcessingThread(QThread):
    def __init__(self,output_queue_ROI,processed_frame_signal,DIC_Result_queue_ROI,int_valor_process):
        super().__init__()
        self.output_queue_ROI = output_queue_ROI
        self.processed_frame_signal = processed_frame_signal
        self.DIC_Result_queue_ROI = DIC_Result_queue_ROI
        self.int_valor_process = int_valor_process
        self.flag_interno = True
    def run(self):
        while self.flag_interno:    
            if not self.output_queue_ROI.empty():
                frame_ROI_processed = self.output_queue_ROI.get()  
                qt_ROI = QImage(frame_ROI_processed.data, frame_ROI_processed.shape[1], frame_ROI_processed.shape[0], frame_ROI_processed.strides[0], QImage.Format.Format_BGR888)#Format_Grayscale8
                self.processed_frame_signal.emit(qt_ROI)
                QThread.msleep(20)
            if not self.DIC_Result_queue_ROI.empty():
                self.actualizar_cordenadas(self.int_valor_process,self.DIC_Result_queue_ROI)

    def actualizar_cordenadas(self, Valor_process,dic_roi):
        global cords_ROI_1,cords_ROI_2, cords_ROI_3, cords_ROI_4
        if Valor_process == 1:
            cords_ROI_1 = dic_roi.get()
        elif Valor_process == 2:
            cords_ROI_2 = dic_roi.get()
        elif Valor_process == 3:
            cords_ROI_3 = dic_roi.get()
        elif Valor_process == 4:
            cords_ROI_4 = dic_roi.get()

    def finalizar_process_interno(self):
        self.flag_interno = False
               
class Creadordesliders(QThread):
    update_signal = pyqtSignal(str, int)

    def __init__(self, sliders):
        super().__init__()
        self.sliders = sliders

    def run(self):
        for slider_name, slider in self.sliders.items():
            self.update_signal.emit(slider_name, slider.value())
            self.msleep(1000)  # Ajusta el tiempo de espera según tus necesidades
        print("creadoresdesliders termino")  

class DICThread(QThread):
    actualizar_signal = pyqtSignal(str, int)
    actualizar_signal_cords = pyqtSignal(str, int, int)
    enviar_signal = pyqtSignal(dict)
    def __init__(self):
        super().__init__()
        self.diccionario_datos = {"Tonalidad Minima S1": 0, "Tonalidad Maxima S1": 255, "Pureza Minima S1": 60,"Pureza Maxima S1": 255,"Luminosidad Minima S1":50,"Luminosidad Maxima S1":255,"Kernel X S1":1,"Kernel Y S1" :1,
                                  "Tonalidad Minima S2": 0, "Tonalidad Maxima S2": 255, "Pureza Minima S2": 60,"Pureza Maxima S2": 255,"Luminosidad Minima S2":50,"Luminosidad Maxima S2":255,"Kernel X S2":1,"Kernel Y S2" :1,
                                  "Tonalidad Minima S3": 0, "Tonalidad Maxima S3": 255, "Pureza Minima S3": 60,"Pureza Maxima S3": 255,"Luminosidad Minima S3":50,"Luminosidad Maxima S3":255,"Kernel X S3":1,"Kernel Y S3" :1,
                                  "Tonalidad Minima S4": 0, "Tonalidad Maxima S4": 255, "Pureza Minima S4": 60,"Pureza Maxima S4": 255,"Luminosidad Minima S4":50,"Luminosidad Maxima S4":255,"Kernel X S4":1,"Kernel Y S4" :1,
                                  "Origen de ROI color 1 X": 0, "Origen de ROI color 1 Y": 0,"width_height ROI color 1 X": 0,"width_height ROI color 1 Y": 0,
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
        
#############################################################################################

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
            print(f"Excepción en el hilo de ejecución: {e}")
    
    def Iniciar_variables_ventana_principal(self):
        self.input_queue_ROI1 = multiprocessing.Queue(maxsize= 5)
        self.input_queue_ROI2 = multiprocessing.Queue(maxsize= 5)
        self.input_queue_ROI3 = multiprocessing.Queue(maxsize= 5)
        self.input_queue_ROI4 = multiprocessing.Queue(maxsize= 5)
        self.dic_thread = DICThread()
        self.video_thread = VideoStreamThread(self.input_queue_ROI1,self.input_queue_ROI2,self.input_queue_ROI3,self.input_queue_ROI4)
        ###########-----------------------------------------------------------------------------------------
        #estos parametros cambian dependidendo de la camara que se use
        




            
#generacion de UI Principal-----------------------------------------
    def inicializarUI(self):
        self.setGeometry(250,100,1250,750)
        self.setWindowTitle("Interfaz_v7.0") 
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
        self.dock1.setAllowedAreas(
            Qt.DockWidgetArea.AllDockWidgetAreas
        )
        self.contenedor_de_widgets = QWidget()
        main_box_dock1 = QGridLayout()
        text1 = QLabel("Distancias entre marcas")
        text1.setFixedHeight(20)
        text1.setStyleSheet("background-color: #dadada")
        main_box_dock1.addWidget(text1, 1, 0,1,2)
        #Ingreso de datos-----------------------------------------------------------------
        main_box_dock1.addWidget(QLabel('Distancia Rojo,Amarillo(cm):'), 2, 0)
        main_box_dock1.addWidget(QLineEdit(), 2, 1)
        main_box_dock1.addWidget(QLabel('Distancia Rojo,Azul(cm):'), 3, 0)
        main_box_dock1.addWidget(QLineEdit(echoMode=QLineEdit.EchoMode.Password), 3, 1)
        main_box_dock1.addWidget(QPushButton('Modificar'), 4, 0,1,2)
        
        #Filtro RGB---------------------------------------------------------------
        text2 = QLabel("Filtro RGB")
        text2.setFixedHeight(20)
        text2.setStyleSheet("background-color: #dadada")
        main_box_dock1.addWidget(text2, 6, 0,1,2)

        self.Widgget_contenedor_de_sliders = QWidget()
        self.tab_widget = QTabWidget(self.Widgget_contenedor_de_sliders)
        

        # Crear pestañas con contenido diferente#"Tonalidad Minima S1": 0, "Tonalidad Maxima S1": 255, "Pureza Minima S1": 60,"Pureza Maxima S1": 255,"Luminosidad Minima S1":50,"Luminosidad Maxima S1":255,"Kernel X S1":1,"Kernel Y S1" :1,
                                  
        tab1 = QWidget()
        self.sliders_tab1 = self.create_elements(tab1, [
            {"type": "slider", "name": "Tonalidad Minima S1", "min": 0, "max": 255, "initial_value": 0, "tick_interval": 10},
            {"type": "slider", "name": "Tonalidad Maxima S1", "min": 0, "max": 255, "initial_value": 255, "tick_interval": 10},
            {"type": "slider", "name": "Pureza Minima S1", "min": 0, "max": 255, "initial_value": 60, "tick_interval": 5},
            {"type": "slider", "name": "Pureza Maxima S1", "min": 0, "max": 255, "initial_value": 255, "tick_interval": 5},
            {"type": "slider", "name": "Luminosidad Minima S1", "min": 0, "max": 255, "initial_value": 50, "tick_interval": 10},
            {"type": "slider", "name": "Luminosidad Maxima S1", "min": 0, "max": 255, "initial_value": 255, "tick_interval": 20},
            {"type": "slider", "name": "Kernel X S1", "min": 0, "max": 2, "initial_value": 1, "tick_interval": 1},
            {"type": "slider", "name": "Kernel Y S1", "min": 0, "max": 2, "initial_value": 1, "tick_interval": 1}
        ])

        tab2 = QWidget()
        self.sliders_tab2 = self.create_elements(tab2, [
            {"type": "slider", "name": "Tonalidad Minima S2", "min": 0, "max": 255, "initial_value": 0, "tick_interval": 10},
            {"type": "slider", "name": "Tonalidad Maxima S2", "min": 0, "max": 255, "initial_value": 255, "tick_interval": 10},
            {"type": "slider", "name": "Pureza Minima S2", "min": 0, "max": 255, "initial_value": 60, "tick_interval": 5},
            {"type": "slider", "name": "Pureza Maxima S2", "min": 0, "max": 255, "initial_value": 255, "tick_interval": 5},
            {"type": "slider", "name": "Luminosidad Minima S2", "min": 0, "max": 255, "initial_value": 50, "tick_interval": 10},
            {"type": "slider", "name": "Luminosidad Maxima S2", "min": 0, "max": 255, "initial_value": 255, "tick_interval": 20},
            {"type": "slider", "name": "Kernel X S2", "min": 0, "max": 2, "initial_value": 1, "tick_interval": 1},
            {"type": "slider", "name": "Kernel Y S2", "min": 0, "max": 2, "initial_value": 1, "tick_interval": 1}
        ])
        tab3 = QWidget()
        self.sliders_tab3 = self.create_elements(tab3, [
            {"type": "slider", "name": "Tonalidad Minima S3", "min": 0, "max": 255, "initial_value": 0, "tick_interval": 10},
            {"type": "slider", "name": "Tonalidad Maxima S3", "min": 0, "max": 255, "initial_value": 255, "tick_interval": 10},
            {"type": "slider", "name": "Pureza Minima S3", "min": 0, "max": 255, "initial_value": 60, "tick_interval": 5},
            {"type": "slider", "name": "Pureza Maxima S3", "min": 0, "max": 255, "initial_value": 255, "tick_interval": 5},
            {"type": "slider", "name": "Luminosidad Minima S3", "min": 0, "max": 255, "initial_value": 50, "tick_interval": 10},
            {"type": "slider", "name": "Luminosidad Maxima S3", "min": 0, "max": 255, "initial_value": 255, "tick_interval": 20},
            {"type": "slider", "name": "Kernel X S3", "min": 0, "max": 2, "initial_value": 1, "tick_interval": 1},
            {"type": "slider", "name": "Kernel Y S3", "min": 0, "max": 2, "initial_value": 1, "tick_interval": 1}
        ])
        tab4 = QWidget()
        self.sliders_tab4 = self.create_elements(tab4, [
            {"type": "slider", "name": "Tonalidad Minima S4", "min": 0, "max": 255, "initial_value": 0, "tick_interval": 10},
            {"type": "slider", "name": "Tonalidad Maxima S4", "min": 0, "max": 255, "initial_value": 255, "tick_interval": 10},
            {"type": "slider", "name": "Pureza Minima S4", "min": 0, "max": 255, "initial_value": 60, "tick_interval": 5},
            {"type": "slider", "name": "Pureza Maxima S4", "min": 0, "max": 255, "initial_value": 255, "tick_interval": 5},
            {"type": "slider", "name": "Luminosidad Minima S4", "min": 0, "max": 255, "initial_value": 50, "tick_interval": 10},
            {"type": "slider", "name": "Luminosidad Maxima S4", "min": 0, "max": 255, "initial_value": 255, "tick_interval": 20},
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
        scroll_area.setMaximumHeight(200)

        

        # Agregar las pestañas al QTabWidget
        
        self.tab_widget.addTab(tab1, "Tab 1")
        self.tab_widget.addTab(tab2, "Tab 2")
        self.tab_widget.addTab(tab3, "Tab 3")
        self.tab_widget.addTab(tab4, "Tab 4")
        

        self.worker_thread = Creadordesliders({**self.sliders_tab1, **self.sliders_tab2, **self.sliders_tab3, **self.sliders_tab4})
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
        
        ventana_video_principal = MiVentana(self.video_thread,self.dic_thread,self.midockwidget)
        tab_bar.addTab(ventana_video_principal,"contenedor1")
        self.contenedor2 = QWidget()
        tab_bar.addTab(self.contenedor2,"contenedor2")
        main_container = QWidget()


        tab_h_box = QHBoxLayout()
        tab_h_box.addWidget(tab_bar)
        main_container.setLayout(tab_h_box)
        self.setCentralWidget(main_container)
    
    def create_dock_2(self):
        self.midockwidget = MiDockWidget(self.video_thread,self.dic_thread,self.input_queue_ROI1,self.input_queue_ROI2,self.input_queue_ROI3,self.input_queue_ROI4)
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
    cords_ROI_1 = None
    cords_ROI_2 = None
    cords_ROI_3 = None
    cords_ROI_4 = None
    calibration_factor = 0.7283353225169037
    camera_matrix = np.array([[695.41363501, 0, 316.72866174],
                              [0, 690.8243246, 238.12973815],
                              [0, 0, 1]])
    distortion_parameters = np.array([[0.2147207, -1.43701464, -0.00359401, 0.00228601, 1.99576813]])
    # Obtiene la información de la CPU

    app = QApplication(sys.argv)
    ventana = Ventana_Principal()
    sys.exit(app.exec())
