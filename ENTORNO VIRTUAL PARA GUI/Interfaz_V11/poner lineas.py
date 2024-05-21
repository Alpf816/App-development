import cv2
import numpy as np
# Función para dibujar una línea de ayuda en el eje X
def draw_x_line(image, x_pos):
    cv2.line(image, (x_pos, 0), (x_pos, image.shape[0]), (0, 255, 0), 2)

# Función para dibujar una línea de ayuda en el eje Y
def draw_y_line(image, y_pos):
    cv2.line(image, (0, y_pos), (image.shape[1], y_pos), (0, 255, 0), 2)

# Función para cambiar la esquina de la imagen
def change_image_corner(image, x_pos, y_pos):
    # Definir las coordenadas de los puntos de la imagen original
    original_pts = np.float32([[0, 0], [image.shape[1], 0], [0, image.shape[0]], [image.shape[1], image.shape[0]]])
    
    # Definir las coordenadas de los puntos de destino (nueva esquina)
    destination_pts = np.float32([[x_pos, y_pos], [image.shape[1], 0], [0, image.shape[0]], [image.shape[1], image.shape[0]]])
    
    # Calcular la matriz de transformación
    matrix = cv2.getPerspectiveTransform(original_pts, destination_pts)
    
    # Aplicar la transformación de perspectiva
    result = cv2.warpPerspective(image, matrix, (image.shape[1], image.shape[0]))
    
    return result
# Leer la imagen
image1 = cv2.imread('Placa de montaje.jpg')
image = cv2.resize(image1, (800, int(800 / image1.shape[1] * image1.shape[0])))


# Obtener datos de Arduino (simulado)
pot1_value = 450
pot2_value = 700
enable_x_line = True
enable_y_line = True
change_corner = False

# Mapear los valores de los potenciómetros al tamaño de la imagen
mapped_x = int(pot1_value * image.shape[1] / 1024)
mapped_y = int(pot2_value * image.shape[0] / 1024)

# Aplicar las funciones correspondientes según los datos de Arduino
if enable_x_line:
    draw_x_line(image, mapped_x)

if enable_y_line:
    draw_y_line(image, mapped_y)

if change_corner:
    change_image_corner(image, mapped_x, mapped_y)

# Mostrar la imagen modificada
cv2.imshow('Modified Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
