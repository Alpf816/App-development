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
                            QGridLayout,
                            QFrame)
from PyQt6.QtGui import * 
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
        self.setWindowTitle("Interfaz_v2.1") 
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
        main_box_dock1 = QGridLayout()
        text2 = QLabel("Distancias entre marcas")
        text2.setStyleSheet("background-color: #dadada")
        main_box_dock1.addWidget(text2, 1, 0,1,2)
        #Ingreso de datos-----------------------------------------------------------------
        main_box_dock1.addWidget(QLabel('Distancia Rojo,Amarillo(cm):'), 2, 0)
        main_box_dock1.addWidget(QLineEdit(), 2, 1)
        main_box_dock1.addWidget(QLabel('Distancia Rojo,Azul(cm):'), 3, 0)
        main_box_dock1.addWidget(QLineEdit(echoMode=QLineEdit.EchoMode.Password), 3, 1)
        main_box_dock1.addWidget(QPushButton('Log in'), 4, 0,alignment=Qt.AlignmentFlag.AlignRight)
        main_box_dock1.addWidget(QPushButton('Close'), 4, 1,alignment=Qt.AlignmentFlag.AlignRight)
        #Filtro RGB---------------------------------------------------------------
        text2 = QLabel("Filtro RGB")
        text2.setStyleSheet("background-color: #dadada")
        main_box_dock1.addWidget(text2, 6, 0,1,2)

        contenedor_de_Filtro_RGB_layout = QVBoxLayout()
        contenedor_de_Filtro_RGB = QWidget()
        tab_bar_filtro_RGB = QTabWidget()

        self.Filtro1 = QWidget()
        self.Filtro2 = QWidget()
        self.Filtro3 = QWidget()
        self.Filtro4 = QWidget()

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
