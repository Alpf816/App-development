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
                            QListWidget)
from PyQt6.QtGui import QPixmap,QAction,QKeySequence
from PyQt6.QtCore import Qt

class Ventana_Principal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.inicializarUI()
        self.barra_de_estado = QStatusBar()
        self.setStatusBar(self.barra_de_estado)
####esta es la principal...................................................................
    def inicializarUI(self):
        self.setGeometry(100,100,1400,750)
        self.setWindowTitle("Interfaz_v1.0") 
        self.create_dock1()
        self.create_dock2()
        self.generate_main_window()
        self.create_menu()
        
        self.show()
#####esta es una secundaria..................................................
    def generate_main_window(self):
        tab_bar = QTabWidget(self)
        self.contenedor1 = QWidget()
        tab_bar.addTab(self.contenedor1,"contenedor1")
        self.contenedor2 = QWidget()
        tab_bar.addTab(self.contenedor2,"contenedor2")
        self.datos_tab()
        tab_h_box = QHBoxLayout()
        tab_h_box.addWidget(tab_bar)

        main_container = QWidget()
        main_container.setLayout(tab_h_box)
        self.setCentralWidget(main_container)

    def datos_tab(self):
        main_v_box = QVBoxLayout()
        button_h_box = QHBoxLayout()
        button_1 = QPushButton("1")
        button_2 = QPushButton("2")
        button_h_box.addWidget(button_1)
        button_h_box.addWidget(button_2)
        button_container = QWidget()
        button_container.setLayout(button_h_box)

        main_v_box.addWidget(button_container)
        self.contenedor1.setLayout(main_v_box)

    def create_dock1(self):
        self.dock1 = QDockWidget()
        self.dock1.setWindowTitle("Modificacion de datos")
        self.dock1.setAllowedAreas(
            Qt.DockWidgetArea.AllDockWidgetAreas
        )
        self.dock1.setAllowedAreas(
            Qt.DockWidgetArea.RightDockWidgetArea
        )
        

        self.contenedor_de_widgets = QWidget()
        main_v_box_dock1 = QVBoxLayout()
        button_11 = QPushButton("1")
        button_22 = QPushButton("2")
        main_v_box_dock1.addWidget(button_11)
        main_v_box_dock1.addWidget(button_22)
        self.contenedor_de_widgets.setLayout(main_v_box_dock1)


        

        self.dock1.setWidget(self.contenedor_de_widgets)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea,self.dock1)

        


    def create_dock2(self):
        self.list2 = QListWidget()
        self.dock2 = QDockWidget()
        self.dock2.setWindowTitle("Mascara y Resultados")
        self.dock2.setAllowedAreas(
            Qt.DockWidgetArea.AllDockWidgetAreas
        )
        self.dock2.setWidget(self.list2)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea,self.dock2)


    def create_menu(self):
        self.menuBar()
        menu_view = self.menuBar().addMenu("Menú")





if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = Ventana_Principal()
    sys.exit(app.exec())
