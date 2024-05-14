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

    def inicializarUI(self):
        self.setGeometry(100,100,1400,750)
        self.setWindowTitle("Interfaz_v1.0") 
        self.generate_main_window()
        #self.generate_tab_bar()
        self.show()
        
    def generate_main_window(self):
        self.generate_tab_bar()

    def generate_tab_bar(self):
        tab_bar = QTabWidget(self)
        self.contenedor1 = QWidget()
        tab_bar.addTab(self.contenedor1,"contenedor1")
        self.contenedor2 = QWidget()
        tab_bar.addTab(self.contenedor2,"contenedor2")
        
        tab_h_box = QHBoxLayout()
        tab_h_box.addWidget(tab_bar)

        main_container = QWidget()
        main_container.setLayout(tab_h_box)
        self.setCentralWidget(main_container)
    



   
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = Ventana_Principal()
    sys.exit(app.exec())
        