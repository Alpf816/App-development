import cv2

# Abrir la cámara y establecer la primera resolución
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Comprobar si la cámara se ha abierto correctamente
if not cap.isOpened():
    print("Error: No se pudo abrir la cámara.")
    exit()

# Tomar una captura en la primera resolución
ret1, frame1 = cap.read()
cv2.imwrite("frame_1280x720.jpg", frame1)
if not ret1:
    print("Error: No se pudo capturar un fotograma en la primera resolución.")
    exit()

# Liberar la captura de video
cap.release()

# Volver a abrir la cámara con la segunda resolución
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Comprobar si la cámara se ha abierto correctamente
if not cap.isOpened():
    print("Error: No se pudo abrir la cámara.")
    exit()

# Tomar una captura en la segunda resolución
ret2, frame2 = cap.read()
cv2.imwrite("frame_640x480.jpg", frame2)
if not ret2:
    print("Error: No se pudo capturar un fotograma en la segunda resolución.")
    exit()

# Liberar la captura de video
cap.release()

# Guardar las imágenes capturadas


