import sys
from PyQt6.QtCore import Qt, QThread, QMutex, QMutexLocker, pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget

class MiThread(QThread):
    actualizar_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.mi_diccionario = {}
        self.mutex = QMutex()

    def agregar_o_modificar(self, nombre, valor):
        with QMutexLocker(self.mutex):
            # Verificar si el nombre ya está en el diccionario
            if nombre in self.mi_diccionario:
                # Si existe, actualizar el valor
                self.mi_diccionario[nombre] = valor
            else:
                # Si no existe, agregar un nuevo ítem
                self.mi_diccionario[nombre] = valor

            # Emitir la señal para actualizar la interfaz gráfica
            self.actualizar_signal.emit(f"Diccionario actualizado: {self.mi_diccionario}")

    def run(self):
        # Ejemplo de uso: ejecutar agregar_o_modificar en otro hilo
        self.agregar_o_modificar("clave3", 40)
        self.agregar_o_modificar("clave4", 50)
        
        self.agregar_o_modificar("clave3", 60)

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.label = QLabel("Esperando actualizaciones...", self)
        self.button = QPushButton("Iniciar Hilo", self)
        self.button.clicked.connect(self.iniciar_hilo)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

        self.mi_thread = MiThread()
        self.mi_thread.actualizar_signal.connect(self.actualizar_label)

    def iniciar_hilo(self):
        self.mi_thread.start()

    def actualizar_label(self, mensaje):
        self.label.setText(mensaje)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())
