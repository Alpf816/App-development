import numpy as np
import cv2

# Función para calcular la matriz de transformación
def calcular_matriz_transformacion(vertices_rombo, tamaño_celda):
    # Definir los puntos del cuadrado en la imagen transformada
    puntos_cuadrado = np.array([[0, 0], [tamaño_celda, 0], [tamaño_celda, tamaño_celda], [0, tamaño_celda]], dtype=np.float32)
    # Calcular la matriz de transformación
    matriz_transformacion = cv2.getPerspectiveTransform(vertices_rombo, puntos_cuadrado)
    return matriz_transformacion

# Coordenadas de los vértices del cuadrado en la imagen original
data_1 = {'corners_reales': [(106, 137), (104, 72), (172, 60), (179, 132)]}

# Obtener las coordenadas de los vértices del cuadrado
corners_reales = data_1['corners_reales']

# Calcular las coordenadas del vértice superior izquierdo del cuadrado original
x_orig, y_orig = corners_reales[1]  # Coordenadas del segundo vértice (el más cercano al origen)

# Restar las coordenadas del vértice superior izquierdo del cuadrado original a todas las coordenadas de los vértices
vertices_rombo_original = np.array([[x - x_orig, y - y_orig] for x, y in corners_reales], dtype=np.float32)

# Tamaño de la celda (supongo que lo mantendremos como en el código anterior)
tamaño_celda = 50

# Calcular la matriz de transformación
matriz_transformacion = calcular_matriz_transformacion(vertices_rombo_original, tamaño_celda)

# Imprimir la matriz de transformación
print("Matriz de Transformación:")
print(matriz_transformacion)
