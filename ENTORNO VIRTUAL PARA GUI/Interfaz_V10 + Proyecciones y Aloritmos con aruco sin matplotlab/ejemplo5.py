import numpy as np
import cv2

# Función para crear una cuadrícula
def crear_cuadricula(filas, columnas, tamaño_celda):
    lienzo = np.ones((filas * tamaño_celda, columnas * tamaño_celda, 3), dtype=np.uint8) * 255
    for i in range(filas):
        for j in range(columnas):
            cv2.rectangle(lienzo, (j * tamaño_celda, i * tamaño_celda), ((j + 1) * tamaño_celda, (i + 1) * tamaño_celda), (0, 0, 0), 1)
    return lienzo

# Función para aplicar una transformación a la cuadrícula
def aplicar_transformacion(lienzo, matriz_transformacion):
    filas, columnas = lienzo.shape[:2]
    lienzo_transformado = cv2.warpAffine(lienzo, matriz_transformacion, (columnas, filas))
    return lienzo_transformado

# Matriz de transformación 2x3 de ejemplo (escala)
matriz_transformacion = np.array([[1, 0.1, 0],
                                   [0.1, 1, 0]], dtype=np.float32)

# Tamaño de la cuadrícula
filas, columnas = 8, 8
tamaño_celda = 50

# Crear la cuadrícula
cuadricula_original = crear_cuadricula(filas, columnas, tamaño_celda)

# Aplicar la transformación a la cuadrícula
cuadricula_transformada = aplicar_transformacion(cuadricula_original, matriz_transformacion)

# Mostrar la cuadrícula original
cv2.imshow("Cuadrícula Original", cuadricula_original)

# Mostrar la cuadrícula transformada
cv2.imshow("Cuadrícula Transformada", cuadricula_transformada)

cv2.waitKey(0)
cv2.destroyAllWindows()
