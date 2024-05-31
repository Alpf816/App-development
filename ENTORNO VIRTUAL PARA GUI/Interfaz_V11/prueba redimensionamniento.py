import cv2
import numpy as np

# Función para dibujar una línea de ayuda en el eje X
def draw_x_line(image, x_pos):
    cv2.line(image, (x_pos, 0), (x_pos, image.shape[0]), (0, 255, 0), 10)

# Función para dibujar una línea de ayuda en el eje Y
def draw_y_line(image, y_pos):
    cv2.line(image, (0, y_pos), (image.shape[1], y_pos), (0, 255, 0), 10)

# Función para cambiar la esquina de la imagen
def change_image_corner(image, x_pos, y_pos):
    # Definir las coordenadas de los puntos de la imagen original
    original_pts = np.float32([[0, 0], [image.shape[1]-100, 0], [0, image.shape[0]-100], [image.shape[1]+400, image.shape[0]-100]])
    
    # Definir las coordenadas de los puntos de destino (nueva esquina)
    destination_pts = np.float32([[image.shape[1]*0.05, image.shape[0]*0.08],[image.shape[1]*0.85, image.shape[0]*0.06],[image.shape[1]*0.1, image.shape[0]*0.76],[image.shape[1]*0.95, image.shape[0]*0.9]])
    
    # Calcular la matriz de transformación
    matrix = cv2.getPerspectiveTransform(original_pts, destination_pts)
    
    # Aplicar la transformación de perspectiva
    result = cv2.warpPerspective(image, matrix, (image.shape[1], image.shape[0]))
    
    return result

# Leer la imagen
image1 = cv2.imread('App-development/ENTORNO VIRTUAL PARA GUI/Interfaz_V10 + Proyecciones y Aloritmos con aruco sin matplotlab/Placa de montaje1.png', cv2.IMREAD_UNCHANGED)
if image1 is None:
    print("Error al leer la imagen.")
else:
    # Separar la imagen y el canal alfa
    bgra_planes = cv2.split(image1)
    image = cv2.merge(bgra_planes[:3])

# Obtener datos de Arduino (simulado)
pot1_value = 700
pot2_value = 600
enable_x_line = True
enable_y_line = True
change_corner = True  # Cambiado a True para activar la transformación de esquina

# Mapear los valores de los potenciómetros al tamaño de la imagen
mapped_x = int(pot1_value * image.shape[1] / 1024)
mapped_y = int(pot2_value * image.shape[0] / 1024)

# Aplicar las funciones correspondientes según los datos de Arduino
if enable_x_line:
    draw_x_line(image, mapped_x)

if enable_y_line:
    draw_y_line(image, mapped_y)

if change_corner:
    # Aplicar la transformación de la esquina de la imagen
    image = change_image_corner(image, mapped_x, mapped_y)

image = cv2.resize(image, (800, int(800 / image.shape[1] * image.shape[0])))

# Mostrar la imagen modificada
cv2.imshow('Modified Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
