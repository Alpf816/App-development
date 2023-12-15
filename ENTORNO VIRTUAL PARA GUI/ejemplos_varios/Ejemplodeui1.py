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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.inicializarUI()
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
            
    def inicializarUI(self):
        self.setGeometry(100,100,1400,750)
        self.setWindowTitle("GUI_deteccion_de_colores_y_mascara_V5")
        self.generate_main_window()
        self.create_dock()
        self.create_action()
        self.create_menu()
        self.show()
    
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

    def create_action(self):
        self.Modificacion_de_datos = QAction('Modificacion de datos',self,checkable=True)
        self.Modificacion_de_datos.setShortcut(QKeySequence("ctrl+L"))
        self.Modificacion_de_datos.setStatusTip("Aqui se pueden modificar los parametros generales del progama")
        self.Modificacion_de_datos.triggered.connect(self.Modificar_datosB)

    def create_dock(self):
        self.list1 = QListWidget()
        self.dock = QDockWidget()
        self.dock.setWindowTitle("Modificacion de datos")
        self.dock.setAllowedAreas(
            Qt.DockWidgetArea.AllDockWidgetAreas
        )
        self.dock.setWidget(self.list1)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea,self.dock)


    def create_menu(self):
        self.menuBar()
        menu_view = self.menuBar().addMenu("Menú")
        menu_view.addAction(self.Modificacion_de_datos)

    def Modificar_datosB(self):
        if self.Modificacion_de_datos.isChecked():
            pass
        else:
            pass
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = MainWindow()
    sys.exit(app.exec())