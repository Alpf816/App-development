import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt

class BorderToggleApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Cambiar entre Bordes y Sin Bordes')
        self.setGeometry(100, 100, 400, 300)

        self.button_toggle = QPushButton('Cambiar Modo', self)
        self.button_toggle.clicked.connect(self.toggle_border_mode)

        layout = QVBoxLayout()
        layout.addWidget(self.button_toggle)
        self.setLayout(layout)

        self.with_border = True
        self.toggle_border_mode()

    def toggle_border_mode(self):
        if self.with_border:
            self.setWindowFlag(Qt.WindowType.FramelessWindowHint, True)  # Establecer sin bordes
            self.with_border = False
        else:
            self.setWindowFlag(Qt.WindowType.FramelessWindowHint, False)  # Establecer con bordes
            self.with_border = True
        self.show()  # Mostrar cambios

def main():
    app = QApplication(sys.argv)
    window = BorderToggleApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
