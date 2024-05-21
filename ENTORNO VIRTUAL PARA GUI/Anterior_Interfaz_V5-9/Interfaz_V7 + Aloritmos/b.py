import numpy as np
import cv2
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Definir el rectángulo en el plano XY
rectangle_points = np.array([[0, 0, 0],
                             [10, 0, 0],
                             [10, 10, 0],
                             [0, 10, 0]], dtype=np.float32)

# Rotar el rectángulo 45 grados en torno al eje Z
angle = np.radians(45)
rotation_matrix = np.array([[np.cos(angle), -np.sin(angle), 0],
                            [np.sin(angle), np.cos(angle), 0],
                            [0, 0, 1]])
rectangle_points_rotated = np.dot(rectangle_points, rotation_matrix.T)

# Proyectar el patrón rotado sobre el plano XY
projected_points = rectangle_points_rotated[:, :2]

# Trasladar los puntos 2D correspondientes
image_points_translated = np.array([[12, 20],
                                    [22, 30],
                                    [27, 25],
                                    [14, 18]], dtype=np.float32)  # Trasladado 2 unidades en el eje X

# Matriz de cámara (parámetros intrínsecos)
camera_matrix = np.array([[695.41363501, 0,  316.72866174],
                          [0, 690.8243246, 238.12973815],
                          [0, 0, 1]], dtype=np.float32)

# Coeficientes de distorsión (si los hay)
dist_coeffs = np.zeros((4, 1))

# Resolver PnP para estimar la pose
success, rvec, tvec, inliers = cv2.solvePnPRansac(rectangle_points_rotated, image_points_translated, camera_matrix, dist_coeffs)

if success:
    print("Vector de rotación (rvec):")
    print(rvec)
    print("Vector de traslación (tvec):")
    print(tvec)
else:
    print("Error al estimar la pose.")

# Crear una figura 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Dibujar el vector de traslación (tvec)
ax.quiver(0, 0, 0, tvec[0], tvec[1], tvec[2], color='r', label='Vector de traslación')

# Dibujar el patrón rotado proyectado sobre el plano XY
ax.plot(projected_points[[0, 1, 2, 3, 0], 0], projected_points[[0, 1, 2, 3, 0], 1], np.zeros(5), color='gray', linestyle='--', label='Patrón rotado en XY')

# Dibujar los puntos 2D correspondientes en la imagen
ax.scatter(image_points_translated[:, 0], image_points_translated[:, 1], np.zeros_like(image_points_translated[:, 0]), color='r', label='Puntos 2D en la imagen')

# Dibujar el vector de rotación
if success:
    rotation_matrix, _ = cv2.Rodrigues(rvec)
    x_axis = rotation_matrix[:, 0] * 5  # Multiplicado por 5 para mejor visualización
    y_axis = rotation_matrix[:, 1] * 5
    z_axis = rotation_matrix[:, 2] * 5
    origin = np.zeros(3)
    ax.quiver(*origin, *x_axis, color='g', label='Eje X de Rotación')
    ax.quiver(*origin, *y_axis, color='b', label='Eje Y de Rotación')
    ax.quiver(*origin, *z_axis, color='y', label='Eje Z de Rotación')

# Configurar límites y etiquetas
ax.set_xlim([-15, 15])
ax.set_ylim([-15, 15])
ax.set_zlim([-5, 5])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.legend()

# Mostrar el gráfico
plt.show()
