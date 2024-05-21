import cv2
import numpy as np
import multiprocessing as mp
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button, TextBox
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import sys
import random


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(QPixmap)
    def __init__(self,parametros_vectores):
        super().__init__()
        self.parametros_vectores = parametros_vectores
        
    def run(self):
        # Inicia la captura de video
        cap = cv2.VideoCapture(0)
        # Cargar el diccionario de ArUCo
        aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        # Crear el detector ArUCo
        aruco_params = cv2.aruco.DetectorParameters()

        while True:
            ret, frame = cap.read()
            if ret:
                # Detectar ArUCo markers
                corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(frame, aruco_dict, parameters=aruco_params)

                if ids is not None and corners is not None:
                    cv2.aruco.drawDetectedMarkers(frame, corners, ids)
                    global camera_matrix,distortion_parameters,avg_tvec,avg_rvec
                    # Calcular la pose de los ArUCo markers
                    rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners, 0.05, camera_matrix, distortion_parameters)
                    if len(tvecs) > 1:
                        avg_tvec = sum(tvecs) / len(tvecs)
                        avg_rvec = sum(rvecs) / len(rvecs)
                        Dict_pose = {"rvecs":avg_rvec,"tvecs":avg_tvec}
                        self.parametros_vectores.put(Dict_pose)
                        if avg_tvec is not None and len(avg_tvec) > 0:
                            average_tvec = np.mean(avg_tvec, axis=0)
                            # Calcular distancia a la cámara
                            distance_cm = np.linalg.norm(average_tvec[0]) * 1000
                            distance = np.linalg.norm(average_tvec[0])
                            print("Distancia promedio a los marcadores: {:.2f} cm".format(distance_cm))
                    else:
                        avg_tvec = tvecs[0]
                        avg_rvec = rvecs[0]
                    # Dibujar los ejes de la pose de los ArUCo markers
                    for rvecs, tvecs in zip(rvecs, tvecs):
                        cv2.drawFrameAxes(frame, camera_matrix,distortion_parameters, rvecs, tvecs, 0.1)
                # Convierte el marco a formato QImage
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                convertido_a_qimg = QImage(frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888).rgbSwapped()
                pixmap = QPixmap.fromImage(convertido_a_qimg)
                # Envía el QPixmap a la ventana principal
                self.change_pixmap_signal.emit(pixmap)
            else:
                print("Error al capturar el marco.")
                break

        cap.release()

def mostrar_matplotlib_3d(matplotlib_iniciado, cambio_color_queue, parametros_vectores):
    fig = plt.figure(figsize=(10, 5))
    ax3d = fig.add_subplot(121, projection='3d')  # Subgráfico 3D
    ax2d = fig.add_subplot(122)  # Subgráfico 2D

    x_data = [-1, 1]
    y_data = [-1, 1]
    z_data = [-1, 1]
    last_color = 'blue'  # Establecer el color predeterminado inicial

    def actualizar(i):
        try:
            nonlocal last_color  # Para acceder y modificar la variable last_color definida fuera de esta función

            ax3d.clear()
            color = cambio_color_queue.get() if not cambio_color_queue.empty() else last_color
            last_color = color  # Actualizar el último color
            ax3d.plot(x_data, y_data, z_data, color=color)

            # Define los vértices de la pirámide
            vertices = np.array([[1, 1, 0], [-1, 1, 0], [-1, -1, 0], [1, -1, 0], [0, 0, 1]])

            arrow_start = [0, 0, 0]
            arrow_direction = [0, 0, 2]

            if not parametros_vectores.empty():
                dic_parametros = parametros_vectores.get()
                rvecs = dic_parametros["rvecs"]
                # Normalizar los vectores de traslación
                tvecs = dic_parametros["tvecs"]
                rvecs_normalized = np.array(rvecs) / np.linalg.norm(rvecs)
                # Normalizar los vectores de traslación
                tvecs_normalized = np.array(tvecs) / np.linalg.norm(tvecs)
                #arrow_direction = np.dot(vertices, rvecs_1.T)
                rot_matrix, _ = cv2.Rodrigues(rvecs_normalized)
                vertices = np.dot(vertices, rot_matrix.T)

            # Define las caras de la pirámide
            faces = [#[vertices[0], vertices[1], vertices[4]],
                    #[vertices[0], vertices[3], vertices[4]],
                    #[vertices[2], vertices[3], vertices[4]],
                    [vertices[1], vertices[2], vertices[4]],
                    [vertices[0], vertices[1], vertices[2], vertices[3]]]

            # Dibuja la pirámide
            ax3d.add_collection3d(Poly3DCollection(faces, facecolors=color, linewidths=1, edgecolors='r', alpha=0.5))

            # Dibuja la flecha
            ax3d.quiver(*arrow_start, *arrow_direction, color=color)

            # Actualizar gráfico 2D con los valores ingresados en los TextBox
            ax2d.clear()
            ax2d.set_title('Gráfico 2D')
            ax2d.set_xlabel('Distancia (m)')
            ax2d.set_ylabel('Valor')

            # Valores de distancia ingresados en los TextBox
            distancias = [float(dist1.text), float(dist2.text), float(dist3.text)]
            valores = [np.sin(d) for d in distancias]

            ax2d.plot(distancias, valores, marker='o', linestyle='-', color='red')

        except Exception as e:
            print(f"Excepción: {e}")

    ani = FuncAnimation(fig, actualizar, frames=range(100), interval=100)

    # Crear TextBoxes para ingresar la distancia
    axtextbox1 = plt.axes([0.9, 0.35, 0.1, 0.075])
    axtextbox2 = plt.axes([0.9, 0.25, 0.1, 0.075])
    axtextbox3 = plt.axes([0.9, 0.15, 0.1, 0.075])

    dist1 = TextBox(axtextbox1, 'Distancia 1 (m)', initial='1.0')
    dist2 = TextBox(axtextbox2, 'Distancia 2 (m)', initial='2.0')
    dist3 = TextBox(axtextbox3, 'Distancia 3 (m)', initial='3.0')

    # Crear botón para cerrar
    axcerrar = plt.axes([0.81, 0.05, 0.1, 0.075])
    bcerrar = Button(axcerrar, 'Cerrar')

    # Función para cerrar
    def cerrar(event):
        plt.close()
        matplotlib_iniciado.value = False

    # Conectar botón a función para cerrar
    bcerrar.on_clicked(cerrar)

    plt.show()


def iniciar_matplotlib(matplotlib_iniciado, cambio_color_queue,parametros_vectores):
    if not matplotlib_iniciado.value:
        matplotlib_process = mp.Process(target=mostrar_matplotlib_3d, args=(matplotlib_iniciado, cambio_color_queue,parametros_vectores))
        matplotlib_process.start()
        matplotlib_iniciado.value = True


class VentanaPrincipal(QMainWindow):
    def __init__(self, matplotlib_iniciado, cambio_color_queue,parametros_vectores):
        super().__init__()

        self.matplotlib_iniciado = matplotlib_iniciado
        self.cambio_color_queue = cambio_color_queue
        self.parametros_vectores = parametros_vectores
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Control de procesos")
        self.setGeometry(100, 100, 500, 400)

        layout = QVBoxLayout()

        btn_matplotlib = QPushButton("Iniciar Matplotlib")
        btn_matplotlib.clicked.connect(lambda: iniciar_matplotlib(self.matplotlib_iniciado, self.cambio_color_queue,self.parametros_vectores))

        btn_cambiar_color = QPushButton("Cambiar Color")
        btn_cambiar_color.clicked.connect(self.cambiar_color)

        self.label_video = QLabel(self)
        self.label_video.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(btn_matplotlib)
        layout.addWidget(btn_cambiar_color)
        layout.addWidget(self.label_video)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def cambiar_color(self):
        # Generar un color RGB aleatorio
        color = (random.random(), random.random(), random.random())
        self.cambio_color_queue.put(color)

    def closeEvent(self, event):
        # Detener el hilo de video cuando se cierra la ventana
        event.accept()
        QApplication.quit()


if __name__ == '__main__':
    #camera_matrix = np.array([[695.41363501, 0, 316.72866174],[0, 690.8243246, 238.12973815],[0, 0, 1]])# externa
    camera_matrix = np.array([[467.91,0,314],[0,467.91,247.20],[0, 0, 1]])
    distortion_parameters = np.array([[0.078, -0.197, 0.0045, -0.0013, 0.01]])
    matplotlib_iniciado = mp.Value('i', False)
    cambio_color_queue = mp.Queue(maxsize = 5)
    parametros_vectores = mp.Queue(maxsize = 5)

    app = QApplication(sys.argv)
    ventana = VentanaPrincipal(matplotlib_iniciado, cambio_color_queue, parametros_vectores)
    ventana.show()

    # Inicia el hilo de video
    video_thread = VideoThread(parametros_vectores)
    video_thread.change_pixmap_signal.connect(ventana.label_video.setPixmap)
    video_thread.start()

    sys.exit(app.exec())
