import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QPixmap, QScreen
from PyQt6.QtCore import Qt
class ProjectionWindow(QWidget):
    def __init__(self, image_path):
        super().__init__()
        self.setWindowTitle('Visualizador de Imágenes')

        # Obtener la resolución de la segunda pantalla
        self.screen_resolution = self.get_screen_resolution()

        # Configurar la ventana sin bordes y en la posición correcta
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, True)
        self.setGeometry(0, 0, self.screen_resolution.width(), self.screen_resolution.height())

        # Crear y configurar el QLabel para mostrar la imagen
        self.label = QLabel(self)
        self.label.setGeometry(0, 0, self.screen_resolution.width(), self.screen_resolution.height())
        self.label.setPixmap(QPixmap(image_path))

    def get_screen_resolution(self):
        app = QApplication(sys.argv)
        screens = app.screens()
        if len(screens) > 1:
            return screens[1].size()  # Tamaño de la segunda pantalla
        else:
            return app.primaryScreen().size()  # Tamaño de la pantalla principal si solo hay una pantalla

def main(image_path):
    app = QApplication(sys.argv)
    window = ProjectionWindow(image_path)
    window.showFullScreen()  # Mostrar en pantalla completa
    sys.exit(app.exec())

if __name__ == '__main__':
    image_path = "App-development\ENTORNO VIRTUAL PARA GUI\Interfaz_V11\Aruco_6.jpg"  # Reemplaza "tu_imagen.jpg" con la ruta de tu imagen
    main(image_path)