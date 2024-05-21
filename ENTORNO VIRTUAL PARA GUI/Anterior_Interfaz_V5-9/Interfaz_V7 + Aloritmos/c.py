import cv2
import multiprocessing as mp
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

# Función para mostrar el video en vivo
def mostrar_video():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('Video en vivo', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

# Función para mostrar la ventana de Matplotlib
def mostrar_matplotlib():
    fig, ax = plt.subplots()
    x_data = []
    y_data = []

    def actualizar(i):
        x_data.append(i)
        y_data.append(i * i)
        ax.clear()
        ax.plot(x_data, y_data)

    ani = FuncAnimation(fig, actualizar, frames=range(100), interval=100)
    plt.show()

if __name__ == '__main__':
    video_process = mp.Process(target=mostrar_video)
    matplotlib_process = mp.Process(target=mostrar_matplotlib)

    video_process.start()
    matplotlib_process.start()

    video_process.join()
    matplotlib_process.join()
