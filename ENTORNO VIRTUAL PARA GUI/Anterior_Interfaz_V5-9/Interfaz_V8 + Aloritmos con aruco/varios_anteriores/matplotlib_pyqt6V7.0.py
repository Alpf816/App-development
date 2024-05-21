import cv2
import multiprocessing as mp
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
import sys
import random



def mostrar_matplotlib(matplotlib_iniciado, cambio_color_queue):
    fig, ax = plt.subplots()
    x_data = []
    y_data = []
    last_color = 'blue'  # Establecer el color predeterminado inicial

    def actualizar(i):
        nonlocal last_color  # Para acceder y modificar la variable last_color definida fuera de esta función
        x_data.append(i)
        y_data.append(i * i)
        ax.clear()
        color = cambio_color_queue.get() if not cambio_color_queue.empty() else last_color
        last_color = color  # Actualizar el último color
        ax.plot(x_data, y_data, color=color)

    ani = FuncAnimation(fig, actualizar, frames=range(100), interval=100)
    
    # Crear botones
    axcerrar = plt.axes([0.81, 0.05, 0.1, 0.075])
    bcerrar = Button(axcerrar, 'Cerrar')

    # Funciones de los botones
    def cerrar(event):
        plt.close()
        matplotlib_iniciado.value = False

    # Conectar botones a funciones
    bcerrar.on_clicked(cerrar)
 
    plt.show()

def iniciar_matplotlib(matplotlib_iniciado, cambio_color_queue):
    if not matplotlib_iniciado.value:
        matplotlib_process = mp.Process(target=mostrar_matplotlib, args=(matplotlib_iniciado, cambio_color_queue))
        matplotlib_process.start()
        matplotlib_iniciado.value = True

class VentanaPrincipal(QMainWindow):
    def __init__(self, matplotlib_iniciado, cambio_color_queue):
        super().__init__()

        self.matplotlib_iniciado = matplotlib_iniciado
        self.cambio_color_queue = cambio_color_queue
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Control de procesos")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        btn_matplotlib = QPushButton("Iniciar Matplotlib")
        btn_matplotlib.clicked.connect(lambda: iniciar_matplotlib(self.matplotlib_iniciado, self.cambio_color_queue))

        btn_cambiar_color = QPushButton("Cambiar Color")
        btn_cambiar_color.clicked.connect(self.cambiar_color)

        layout.addWidget(btn_matplotlib)
        layout.addWidget(btn_cambiar_color)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def cambiar_color(self):
        # Generar un color RGB aleatorio
        color = (random.random(), random.random(), random.random())
        self.cambio_color_queue.put(color)

if __name__ == '__main__':
    matplotlib_iniciado = mp.Value('i', False)
    cambio_color_queue = mp.Queue()

    app = QApplication(sys.argv)
    ventana = VentanaPrincipal(matplotlib_iniciado, cambio_color_queue)
    ventana.show()

    sys.exit(app.exec())
