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

# Calcular los vértices del rombo transformado
def calcular_vertices_rombo(matriz_transformacion, x, y, tamaño_celda):
    x1, y1 = x, y
    x2, y2 = x + tamaño_celda, y
    x3, y3 = x + tamaño_celda, y + tamaño_celda
    x4, y4 = x, y + tamaño_celda

    # Aplicar la transformación a cada vértice
    puntos = np.array([[x1, y1], [x2, y2], [x3, y3], [x4, y4]], dtype=np.float32)
    puntos_transformados = cv2.transform(puntos.reshape(-1, 1, 2), matriz_transformacion)
    puntos_transformados = puntos_transformados.reshape(-1, 2)
    
    return puntos_transformados

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

# Coordenadas del primer cuadrado en la cuadrícula original
x1_orig, y1_orig = 0, 0
x2_orig, y2_orig = tamaño_celda, tamaño_celda

# Coordenadas del primer cuadrado en la cuadrícula transformada
x1_trans, y1_trans = 0, 0
x2_trans, y2_trans = int(tamaño_celda * 1.1), int(tamaño_celda * 1.1)

# Colores para resaltar los cuadrados
color_orig = (0, 255, 0)  # Verde para la cuadrícula original
color_trans = (0, 0, 255)  # Rojo para la cuadrícula transformada

# Dibujar el primer cuadrado resaltado en la cuadrícula original
cv2.rectangle(cuadricula_original, (x1_orig, y1_orig), (x2_orig, y2_orig), color_orig, -1)

# Calcular los vértices del rombo transformado
vertices_rombo = calcular_vertices_rombo(matriz_transformacion, x1_trans, y1_trans, tamaño_celda)

# Dibujar el rombo resaltado en la cuadrícula transformada
cv2.polylines(cuadricula_transformada, [np.int32(vertices_rombo)], isClosed=True, color=color_trans, thickness=1)

# Mostrar la cuadrícula original
cv2.imshow("Cuadrícula Original", cuadricula_original)

# Mostrar la cuadrícula transformada
cv2.imshow("Cuadrícula Transformada", cuadricula_transformada)

cv2.waitKey(0)
cv2.destroyAllWindows()