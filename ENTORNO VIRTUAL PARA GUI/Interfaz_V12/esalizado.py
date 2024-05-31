import sys
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QPixmap, QScreen,QGuiApplication
from PyQt6.QtCore import Qt

class ProjectionWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Imagen Sin Bordes')
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self.image_path = 'C:/Users/a/Desktop/python-course/App-development/ENTORNO VIRTUAL PARA GUI/Interfaz_V12/Aruco_6.jpg'

        # Cargar la imagen
        pixmap = QPixmap(self.image_path)

        # Crear un QLabel para mostrar la imagen
        self.label = QLabel(self)
        self.label.setPixmap(pixmap)
        # No es necesario establecer setScaledContents(False) para mantener el tamaño original
        #self.label.setScaledContents(False)  

        # Configurar el layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        self.setLayout(layout)

        # Ajustar la posición de la ventana para que el borde quede fuera de la pantalla
        self.adjust_window_position()

    def adjust_window_position(self):
        # Obtener la geometría del QLabel
        label_rect = self.label.geometry()

        # Obtener la lista de pantallas disponibles
        screen_list = QGuiApplication.screens()

        # Verificar si hay al menos dos pantallas disponibles
        if len(screen_list) > 1:
            # Obtener la geometría de la segunda pantalla
            second_screen_geometry = screen_list[1].geometry()

            # Calcular la nueva posición de la ventana
            new_x = int(second_screen_geometry.x() -11 )
            new_y = int(second_screen_geometry.y() -11 )

            # Establecer la nueva posición de la ventana
            self.move(new_x, new_y)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProjectionWindow()
    window.show()
    sys.exit(app.exec())
