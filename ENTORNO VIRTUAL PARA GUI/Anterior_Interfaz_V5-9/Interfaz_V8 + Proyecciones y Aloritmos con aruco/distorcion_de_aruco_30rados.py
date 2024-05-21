import cv2
import numpy as np

# Cargar la imagen del ArUco de tamaño conocido (2x2 cm)
aruco_image = cv2.imread('ENTORNO VIRTUAL PARA GUI\Interfaz_V8 + Proyecciones y Aloritmos con aruco/4x4_1000-6 (1).png')

# Definir los puntos de la imagen original
original_points = np.float32([[0, 0], [aruco_image.shape[1], 0], [0, aruco_image.shape[0]], [aruco_image.shape[1], aruco_image.shape[0]]])

# Definir los puntos de destino con la distorsión de perspectiva
theta = np.radians(30)  # Ángulo de inclinación del proyector
destination_points = np.float32([[0, 0], 
                                 [aruco_image.shape[1], 0], 
                                 [aruco_image.shape[1] * np.cos(theta), aruco_image.shape[1] * np.sin(theta)], 
                                 [aruco_image.shape[1] + aruco_image.shape[1] * np.cos(theta), aruco_image.shape[1] * np.sin(theta)]])

# Calcular la matriz de transformación de perspectiva (homografía)
M = cv2.getPerspectiveTransform(original_points, destination_points)

# Aplicar la transformación de perspectiva a la imagen del ArUco
distorted_aruco = cv2.warpPerspective(aruco_image, M, (aruco_image.shape[1] + int(aruco_image.shape[1] * np.cos(theta)), aruco_image.shape[0]))

# Crear una imagen de fondo blanco del mismo tamaño que la imagen distorsionada
background = np.ones_like(distorted_aruco) * 255

# Definir una máscara binaria para la imagen distorsionada
_, mask = cv2.threshold(distorted_aruco, 240, 255, cv2.THRESH_BINARY)

# Invertir la máscara para obtener la región donde se superpondrá la imagen distorsionada
mask_inv = cv2.bitwise_not(mask).astype(np.uint8)  # Convertir la máscara a tipo de datos adecuado

# Superponer la imagen distorsionada en el fondo blanco usando la máscara
result = cv2.bitwise_and(background, background, mask=mask_inv)

# Agregar la imagen distorsionada a la región donde la máscara está activa
result += cv2.cvtColor(distorted_aruco, cv2.COLOR_GRAY2BGR)

# Mostrar la imagen resultante
cv2.imshow('Distorted ArUco', result)
cv2.waitKey(0)
cv2.destroyAllWindows()