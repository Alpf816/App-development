import imutils
import cv2 
import numpy as np
# datos obtenidos de la calibracion de la camara
CameraMatrix = np.array([[468.16,0,323.37],[0, 467.73,242.79747611],[0,0,1]])
DistorsionParameters = np.array([[0.02274],[-0.2431],[0.000213],[-0.00952],[0.02274]])

camara_celular = cv2.VideoCapture(2)

key = cv2.waitKey(1)
while not key == ord('q'):

    check, frame = camara_celular.read()
    if frame is None:
        break
        
    cv2.imshow("Imagen", frame)
    key = cv2.waitKey(1)
    
cv2.destroyAllWindows()
# La entrada es el frame en formato HSV
def getCentroRojo(frame_hsv):
    #Definimos los limites HSV para elegir el rojo
    limites_rojo = ((0,0,0),(255,255,255))

    #Generamos la mascara y obtenemos los contornos
    mask_rojo = cv2.inRange(frame_hsv, limites_rojo[0], limites_rojo[1])
    cnts, _ = cv2.findContours(mask_rojo, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2:]
    cnts = imutils.grab_contours(cnts)
    
    
    # Si tenemos algún contorno
    if len(cnts) > 0:
       # Buscamos el que tenga más área
       c = max(cnts, key=cv2.contourArea)

       #Cogemos el círculo que más se aproxime. x,y serán las coordenadas de nuestra detección.
       ((x, y), radius) = cv2.minEnclosingCircle(c)
    print("x ="+x+"y ="+y)
    return (x,y)
def getCentroAmarillo(frame_hsv):
    #Definimos los limites HSV para elegir el rojo
    limites_Amarillo = ((162,153,61),(193,255,178))

    #Generamos la mascara y obtenemos los contornos
    mask_Amarillo = cv2.inRange(frame_hsv, limites_Amarillo[0], limites_Amarillo[1])
    cnts, _ = cv2.findContours(mask_Amarillo, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]
    cnts = imutils.grab_contours(cnts)
    
    # Si tenemos algún contorno
    if len(cnts) > 0:
       # Buscamos el que tenga más área
       c = max(cnts, key=cv2.contourArea)

       #Cogemos el círculo que más se aproxime. x,y serán las coordenadas de nuestra detección.
       ((x, y), radius) = cv2.minEnclosingCircle(c)
      
    return (x,y)
def getCentroAzul(frame_hsv):
    #Definimos los limites HSV para elegir el rojo
    limites_Azul = ((162,153,61),(193,255,178))

    #Generamos la mascara y obtenemos los contornos
    mask_Azul = cv2.inRange(frame_hsv, limites_Azul[0], limites_Azul[1])
    cnts, _ = cv2.findContours(mask_Azul, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]
    cnts = imutils.grab_contours(cnts)
    
    # Si tenemos algún contorno
    if len(cnts) > 0:
       # Buscamos el que tenga más área
       c = max(cnts, key=cv2.contourArea)

       #Cogemos el círculo que más se aproxime. x,y serán las coordenadas de nuestra detección.
       ((x, y), radius) = cv2.minEnclosingCircle(c)
      
    return (x,y)
def getCentroVerde(frame_hsv):
    #Definimos los limites HSV para elegir el rojo
    limites_Verde = ((0,0,0),(255,255,255))

    #Generamos la mascara y obtenemos los contornos
    mask_Verde = cv2.inRange(frame_hsv, limites_Verde[0], limites_Verde[1])
    cnts, _ = cv2.findContours(mask_Verde, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]
    cnts = imutils.grab_contours(cnts)
    
    # Si tenemos algún contorno
    if len(cnts) > 0:
       # Buscamos el que tenga más área
       c = max(cnts, key=cv2.contourArea)

       #Cogemos el círculo que más se aproxime. x,y serán las coordenadas de nuestra detección.
       ((x, y), radius) = cv2.minEnclosingCircle(c)
      
    return (x,y)
frame= cv2.cvtColor( ... , cv2.COLOR_BGR2HSV) 
centro_rojo = getCentroRojo(frame)
centro_verde = getCentroVerde(frame)
centro_azul = getCentroAzul(frame)
centro_amarillo = getCentroAmarillo(frame)
patron = np.array([[0, 10], # Punto 1: X = 0, Y = 10
                   [5, 10], # Punto 2: X = 5, Y = 10 
                   [0,  0], # Punto 3: X = 0, Y = 0 (Origen de coordenadas)
                   [5,  0]])# Ultimo punto
centros_ordenados = [ centro_azul , centro_verde, centro_rojo, centro_amarillo ]
ret, rvec, tvec = cv2.solvePnP(patron ,
                         np.array(centros_ordenados),
                         CameraMatrix # Obtenida durante la calibración
                         )  # Obtenido durante la calibración
def CalcularXYZ(u,v, A, rvec, tvec, s):
    # Generamos el vector m
    uv = np.array([[u,v,1]], dtype=np.float).T

    # Obtenemos R a partir de rvec
    R, _ = cv2.Rodrigues(rvec)
    Inv_R = np.linalg.inv(R)
    
    # Parte izquierda m*A^(-1)*R^(-1)
    Izda = Inv_R.dot(np.linalg.inv(A).dot(uv))

    # Parte derecha
    Drch = Inv_R.dot(tvec)

    # Calculamos S porque sabemos Z = 0
    s = 0 + Drch[2][0]/Izda[2][0]
    
    XYZ = Inv_R.dot( s * np.linalg.inv(A).dot(uv) - tvec)
   
    return XYZ
