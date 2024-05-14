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

class MyMainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        

        # Crear instancia del DICThread
        self.dic_thread = DICThread()
        # Conectar la señal actualizar_signal a la función handle_slider_change
        #self.dic_thread.actualizar_signal.connect(self.handle_slider_change)
        

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.tab_widget = QTabWidget(self.central_widget)
        self.setCentralWidget(self.tab_widget)


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
        self.dic_thread.actualizar_signal.connect(self.actualizar_tabla)
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.tab_Datos)

        

        # Agregar las pestañas al QTabWidget
        self.tab_widget.addTab(scroll_area,"Datos enerales")
        self.tab_widget.addTab(tab1, "Tab 1")
        self.tab_widget.addTab(tab2, "Tab 2")
        self.tab_widget.addTab(tab3, "Tab 3")
        self.tab_widget.addTab(tab4, "Tab 4")
        

        self.worker_thread = Creadordesliders({**self.sliders_tab1, **self.sliders_tab2, **self.sliders_tab3})
        self.worker_thread.update_signal.connect(self.handle_slider_change)
        #self.dic_thread.actualizar_signal.connect(self.handle_slider_change)
        self.worker_thread.start()
        self.dic_thread.start()
        self.actualizar_tabla_con_preset()

    def procesar_diccionario_modificado(self, diccionario):
        # Aquí puedes manejar el diccionario modificado en tu ventana principal
        print("Diccionario modificado:", diccionario)

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
                s.setTickInterval(element["tick_interval"])
                s.setTickPosition(QSlider.TickPosition.TicksBelow)

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
        
if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MyMainWindow()
    window.setGeometry(100, 100, 600, 400)
    window.show()

    sys.exit(app.exec())