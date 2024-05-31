import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

def graficar_rectangulo(arucos_set):
    fig, ax = plt.subplots()

    # Obtener puntos extremos
    puntos = list(arucos_set.values())
    puntos = np.array(puntos).reshape(-1, 2)
    min_x, min_y = np.min(puntos, axis=0)
    max_x, max_y = np.max(puntos, axis=0)

    # Dibujar rectángulo
    rectangulo = Polygon([(min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y)], closed=True, fill=None, edgecolor='r')
    ax.add_patch(rectangulo)

    # Dibujar puntos
    for aruco_id, aruco_points in arucos_set.items():
        aruco_points = np.array(aruco_points)
        ax.scatter(aruco_points[:, 0], aruco_points[:, 1], label=f'ArUco {aruco_id}')
        ax.text(aruco_points[:, 0], aruco_points[:, 1], f'ArUco {aruco_id}', fontsize=8, ha='right')

    ax.set_aspect('equal')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Rectángulo con puntos extremos')
    ax.legend()
    plt.show()

arucos_set2 = {
    1: np.array([[511., 329.], [564., 331.], [566., 385.], [512., 383.]]),
    3: np.array([[66., 322.], [119., 323.], [115., 377.], [62., 376.]]),
    2: np.array([[84., 119.], [134., 120.], [130., 169.], [80., 167.]]),
    4: np.array([[503., 126.], [553., 127.], [556., 175.], [505., 175.]])
}

graficar_rectangulo(arucos_set2)
