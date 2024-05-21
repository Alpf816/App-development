import cv2
import multiprocessing as mp
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
import sys



def mostrar_matplotlib(matplotlib_iniciado):
    fig, ax = plt.subplots()
    x_data = []
    y_data = []

    def actualizar(i):
        x_data.append(i)
        y_data.append(i * i)
        ax.clear()
        ax.plot(x_data, y_data)

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

def iniciar_matplotlib(matplotlib_iniciado):
    if not matplotlib_iniciado.value:
        matplotlib_process = mp.Process(target=mostrar_matplotlib, args=(matplotlib_iniciado,))
        matplotlib_process.start()
        matplotlib_iniciado.value = True

class VentanaPrincipal(QMainWindow):
    def __init__(self, matplotlib_iniciado):
        super().__init__()

        self.matplotlib_iniciado = matplotlib_iniciado
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Control de procesos")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        btn_matplotlib = QPushButton("Iniciar Matplotlib")
        btn_matplotlib.clicked.connect(lambda: iniciar_matplotlib(self.matplotlib_iniciado))

        layout.addWidget(btn_matplotlib)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

if __name__ == '__main__':
    matplotlib_iniciado = mp.Value('i', False)

    app = QApplication(sys.argv)
    ventana = VentanaPrincipal(matplotlib_iniciado)
    ventana.show()

    sys.exit(app.exec())
