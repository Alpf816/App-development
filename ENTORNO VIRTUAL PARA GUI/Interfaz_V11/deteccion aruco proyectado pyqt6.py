import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QSlider, QLabel, QGridLayout
from PyQt6.QtCore import Qt

class CustomWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Crear el layout grid para organizar los elementos
        self.layout = QGridLayout()

        # Crear el label para mostrar los frames
        self.label = QLabel("Frames")
        self.layout.addWidget(self.label, 0, 0, 3, 1)  # (fila, columna, rowspan, colspan)

        # Crear botón
        self.button = QPushButton("Botón")
        self.layout.addWidget(self.button, 0, 1)

        # Crear los sliders
        self.slider1 = QSlider(Qt.Orientation.Vertical)
        self.slider2 = QSlider(Qt.Orientation.Vertical)
        self.layout.addWidget(self.slider1, 1, 1)
        self.layout.addWidget(self.slider2, 2, 1)

        # Establecer el layout principal del widget
        self.setLayout(self.layout)

        # Ocultar el botón y los sliders
        self.hide_menu()

    def hide_menu(self):
        # Ocultar el botón y los sliders
        self.button.setHidden(True)
        self.slider1.setHidden(True)
        self.slider2.setHidden(True)

    def show_menu(self):
        # Mostrar el botón y los sliders
        self.button.setHidden(False)
        self.slider1.setHidden(False)
        self.slider2.setHidden(False)

    def enterEvent(self, event):
        # Mostrar el menú cuando el cursor entra en el widget
        self.show_menu()

    def leaveEvent(self, event):
        # Ocultar el menú cuando el cursor sale del widget
        self.hide_menu()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = CustomWidget()
    widget.resize(300, 200)
    widget.show()
    sys.exit(app.exec())
