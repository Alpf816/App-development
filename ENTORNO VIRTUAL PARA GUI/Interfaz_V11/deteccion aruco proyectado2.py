import cv2
import numpy as np

def adjust_brightness_contrast(image, brightness=0, contrast=0):
    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow) / 255
        gamma_b = shadow

        buf = cv2.addWeighted(image, alpha_b, image, 0, gamma_b)
    else:
        buf = image.copy()

    if contrast != 0:
        f = 131 * (contrast + 127) / (127 * (131 - contrast))
        alpha_c = f
        gamma_c = 127 * (1 - f)

        buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)

    return buf

def on_brightness_change(value):
    global brightness
    brightness = value
    update_image()

def on_contrast_change(value):
    global contrast
    contrast = value
    update_image()

def update_image():
    adjusted = adjust_brightness_contrast(gray, brightness, contrast)
    inverted = invert_image(adjusted)
    blurred = cv2.GaussianBlur(inverted, (5, 5), 0)

    cv2.imshow('ArUco Detection', frame)
    cv2.imshow('Filtered Image', adjusted)

    # Detección de ArUcos en la imagen filtrada
    corners, ids, rejected = cv2.aruco.detectMarkers(adjusted, aruco_dict, parameters=parameters)

    # Dibujar los ejes en la imagen original
    if ids is not None:
        for i in range(len(ids)):
            rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners[i], 0.05, camera_matrix, dist_coeffs)
            cv2.drawFrameAxes(frame, camera_matrix, dist_coeffs, rvecs[0], tvecs[0], 0.1)

# Función para invertir la imagen
def invert_image(image):
    return cv2.bitwise_not(image)

# Cargar el diccionario de ArUcos
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
parameters = cv2.aruco.DetectorParameters()

# Parámetros de la cámara (necesitas calibrar tu cámara y usar tus propios valores)
# Aquí se usan valores de ejemplo
camera_matrix = np.array([[467.91, 0, 314.081],
                          [0, 467.91, 247.2],
                          [0, 0, 1]], dtype=float)
dist_coeffs = np.array([0.078, -0.197, 0.0004, 0], dtype=float)

# Capturar la imagen desde la cámara
cap = cv2.VideoCapture(0)

brightness = 0
contrast = 0

# Crear una ventana para los sliders
cv2.namedWindow('Adjustments')
cv2.createTrackbar('Brightness', 'Adjustments', brightness, 100, on_brightness_change)
cv2.createTrackbar('Contrast', 'Adjustments', contrast, 100, on_contrast_change)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Preprocesamiento
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Ajuste de brillo y contraste
    update_image()

    # Dibujar los ejes y mostrar la imagen
    cv2.imshow('ArUco Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()