
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

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('My App')
        self.create_ventana_central()
        self.setGeometry(100,100,1400,750)
        self.setWindowTitle("Interfaz_v1.11") 
        self.show()
        
        # Cannot set QxxLayout directly on the QMainWindow
        # Need to create a QWidget and set it as the central widget
        widget = QWidget()
        layout = QVBoxLayout()
        b1 = QPushButton('Red'   ); b1.setStyleSheet("background-color: red;")
        b2 = QPushButton('Blue'  ); b2.setStyleSheet("background-color: blue;")
        b3 = QPushButton('Yellow'); b3.setStyleSheet("background-color: yellow;")
        layout.addWidget(b1)
        layout.addWidget(b2)
        layout.addWidget(b3)
            
        widget.setLayout(layout)
        

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


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()