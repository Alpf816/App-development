import cv2
import numpy as np

def calcular_escala(arucos_set1, medida_fisica_mm):
    # Calcular la distancia promedio en píxeles entre las esquinas adyacentes de los ArUcos del primer conjunto
    distancias_pixeles = []
    for corners in arucos_set1.values():
        ancho_aruco = np.linalg.norm(corners[0] - corners[1])  # Suponiendo que [0, 1] son esquinas adyacentes
        distancias_pixeles.append(ancho_aruco)
    distancia_promedio_pixeles = np.mean(distancias_pixeles)
    # Calcular la escala en mm/px
    escala = medida_fisica_mm / distancia_promedio_pixeles
    return escala

def calcular_ancho_arucos_proyectados(arucos_set2):
    # Calcular el ancho promedio de los ArUcos del set2 en píxeles
    distancias_pixeles = []
    for corners in arucos_set2.values():
        ancho_aruco = np.linalg.norm(corners[0] - corners[1])  # Suponiendo que [0, 1] son esquinas adyacentes
        distancias_pixeles.append(ancho_aruco)
    
    ancho_arucos_proyectados_px = np.mean(distancias_pixeles)
    return ancho_arucos_proyectados_px

def calcular_tamano_aruco_proyectado(escala, ancho_arucos_proyectados_px):
    # Calcular el tamaño de los ArUcos proyectados en milímetros
    ancho_arucos_proyectados_mm = ancho_arucos_proyectados_px * escala
    return ancho_arucos_proyectados_mm

def mm_por_pixel_en_imagen_proyectada(ancho_arucos_proyectados_mm, ancho_arucos_proyectados_px):
    # Calcular la relación mm/px para la imagen proyectada
    return ancho_arucos_proyectados_mm / ancho_arucos_proyectados_px

# Datos proporcionados
arucos_set1 = {
    1: np.array([[164, 174], [163, 196], [142, 196], [143, 174]]),
    2: np.array([[141, 308], [164, 306], [164, 329], [143, 331]]),
    3: np.array([[277, 175], [275, 196], [254, 195], [255, 174]]),
    4: np.array([[246, 335], [248, 312], [270, 314], [269, 336]])
}

arucos_set2 = {
    1: np.array([[511., 329.], [564., 331.], [566., 385.], [512., 383.]]),
    3: np.array([[66., 322.], [119., 323.], [115., 377.], [62., 376.]]),
    2: np.array([[84., 119.], [134., 120.], [130., 169.], [80., 167.]]),
    4: np.array([[503., 126.], [553., 127.], [556., 175.], [505., 175.]])
}

medida_fisica_mm = 50
ancho_arucos_Antes_de_proyeccion = 200
# Calcular la escala usando el primer conjunto de ArUcos
escala = calcular_escala(arucos_set1, medida_fisica_mm)

# Calcular el tamaño de los ArUcos proyectados en milímetros
ancho_arucos_proyectados_px = calcular_ancho_arucos_proyectados(arucos_set2)
ancho_arucos_proyectados_mm = calcular_tamano_aruco_proyectado(escala, ancho_arucos_proyectados_px)

# Calcular la relación mm/px para la imagen proyectada
mm_por_pixel = mm_por_pixel_en_imagen_proyectada(ancho_arucos_proyectados_mm, ancho_arucos_Antes_de_proyeccion)


# Imprimir los resultados
print(f'Escala (mm/px): {escala}')
print(f'Ancho de los ArUcos proyectados en mm: {ancho_arucos_proyectados_mm}')
print(f'Milímetros por píxel en la imagen proyectada: {mm_por_pixel}')


