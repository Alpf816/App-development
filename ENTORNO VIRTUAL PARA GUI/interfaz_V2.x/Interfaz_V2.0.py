
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
                            QFormLayout,
                            QGridLayout)
from PyQt6.QtGui import QPixmap,QAction,QKeySequence
from PyQt6.QtCore import Qt

class Ventana_Principal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.inicializarUI()
        self.barra_de_estado = QStatusBar()
        self.setStatusBar(self.barra_de_estado)
#generacion de UI Principal-----------------------------------------
    def inicializarUI(self):
        self.setGeometry(100,100,1400,750)
        self.setWindowTitle("Interfaz_v1.11") 
        self.generate_main_window()
        self.created_actions()
        self.show()
#aqui se colocan todas las demas ventanas
    def generate_main_window(self):
        self.create_menu()
        self.create_dock_1()
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
    def create_dock_1(self):
        self.dock1 = QDockWidget()
        self.dock1.setWindowTitle("Modificacion de datos")
        self.dock1.setAllowedAreas(
            Qt.DockWidgetArea.AllDockWidgetAreas
        )
        self.contenedor_de_widgets = QWidget()
        main_v_box_dock1 = QVBoxLayout()
        #Ingreso de datos
        v_box_1 = QVBoxLayout()
        v_box_1_widget = QWidget()
        sub_v_box_h_box_1 = QVBoxLayout
        sub_v_box_h_box_1_widget = QWidget()
        informacion = QLabel("Ingreso de distancias entre puntos")
        informacion2 = QLabel("(Estimación de posición)")
        sub_v_box_h_box_1.addWidget(informacion)
        sub_v_box_h_box_1.addWidget(informacion2)
        sub_h_box_1_sub_v_box_h_box_1 = QVBoxLayout
        sub_h_box_1_sub_v_box_h_box_1_widget = QWidget()
        sub_h_box_1_sub_v_box_h_box_2 = QVBoxLayout
        sub_h_box_1_sub_v_box_h_box_2_widget = QWidget()
        lbl11 = QLabel("Distancia Rojo,Amarillo EJEX")
        self.disX = QLineEdit()
        sub_h_box_1_sub_v_box_h_box_1.addWidget(lbl11)
        sub_h_box_1_sub_v_box_h_box_1.addWidget(self.disX)
        lbl12 = QLabel("Distancia Rojo,Azul EJEY")
        self.disY = QLineEdit()
        sub_h_box_1_sub_v_box_h_box_2.addWidget(lbl12)
        sub_h_box_1_sub_v_box_h_box_2.addWidget(self.disY)

        sub_v_box_h_box_1.addWidget(sub_h_box_1_sub_v_box_h_box_1_widget)
        sub_v_box_h_box_1.addWidget(sub_h_box_1_sub_v_box_h_box_2_widget)
        boton_datos = QPushButton("Sobreescribir Datos")
        sub_v_box_h_box_1.addWidget(boton_datos)
        
        v_box_2 = QVBoxLayout()
        v_box_2_widget = QWidget()

        sub_v_box_h_box_2 = QVBoxLayout()
        sub_v_box_h_box_2_widget = QWidget()
        

        button_1 = QPushButton("1")
        button_2 = QPushButton("2")




        v_box_1_widget.setLayout(v_box_1)
        sub_v_box_h_box_1_widget.setLayout(sub_v_box_h_box_1)
        sub_h_box_1_sub_v_box_h_box_1_widget.setLayout(sub_h_box_1_sub_v_box_h_box_1)
        sub_h_box_1_sub_v_box_h_box_2_widget.setLayout(sub_h_box_1_sub_v_box_h_box_2)
        v_box_2_widget.setLayout(v_box_2)
        sub_v_box_h_box_2_widget.setLayout(sub_v_box_h_box_2)





        main_v_box_dock1.addWidget(v_box_1)
        main_v_box_dock1.addWidget(v_box_2)
        self.contenedor_de_widgets.setLayout(main_v_box_dock1)
        self.dock1.setWidget(self.contenedor_de_widgets)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea,self.dock1)
        

    def create_ventana_central(self):
        tab_bar = QTabWidget(self)
        self.contenedor1 = QWidget()
        tab_bar.addTab(self.contenedor1,"contenedor1")
        self.contenedor2 = QWidget()
        tab_bar.addTab(self.contenedor2,"contenedor2")
        self.datos_Ventana_central_tab()
        tab_h_box = QHBoxLayout()
        tab_h_box.addWidget(tab_bar)
        main_container = QWidget()
        main_container.setLayout(tab_h_box)
        self.setCentralWidget(main_container)

    def datos_Ventana_central_tab(self):
        pass

    

    def create_dock_2(self):
        self.list2 = QListWidget()
        self.dock2 = QDockWidget()
        self.dock2.setWindowTitle("Mascara y Resultados")
        self.dock2.setAllowedAreas(
               Qt.DockWidgetArea.AllDockWidgetAreas
        )
        self.contenedor_de_widgets = QWidget()
        main_v_box_dock2 = QVBoxLayout()
        button_1 = QPushButton("1")
        button_2 = QPushButton("2")
        main_v_box_dock2.addWidget(button_1)
        main_v_box_dock2.addWidget(button_2)
        self.contenedor_de_widgets.setLayout(main_v_box_dock2)
        self.dock2.setWidget(self.contenedor_de_widgets)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea,self.dock2)



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



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = Ventana_Principal()
    sys.exit(app.exec())
