import cv2
import cv2.aruco as aruco

# Función para detectar y dibujar los marcadores ArUco
def detect_aruco_markers(frame, aruco_dict, aruco_params):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=aruco_params)

    if ids is not None:
        aruco.drawDetectedMarkers(frame, corners, ids)

# Configuración de los marcadores ArUco
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
aruco_params = aruco.DetectorParameters()

# Captura de video en vivo
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    detect_aruco_markers(frame, aruco_dict, aruco_params)

    cv2.imshow('ArUco Marker Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
