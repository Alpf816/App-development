# Importamos librerias
from tkinter import *
from PIL import Image, ImageTk
import cv2
import imutils
import numpy as np

# Funcion Visualizar
def visualizar():
    global pantalla, frame, rgb, hsv, gray, slival1, slival11, slival2, slival22, slival3, slival33
    # Leemos la videocaptura
    if cap is not None:
        ret, frame = cap.read()

        # Si es correcta
        if ret == True:

            if (rgb == 1 and hsv == 0 and gray == 0):
                # Color BGR
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            elif rgb == 0 and hsv == 1 and gray == 0:
                # Color HSV
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            elif (rgb == 0 and hsv == 0 and gray == 1):
                # Color GRAY
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


            # Rendimensionamos el video
            frame = imutils.resize(frame, width=640)

            # Convertimos el video
            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)

            # Mostramos en el GUI
            lblVideo.configure(image=img)
            lblVideo.image = img
            lblVideo.after(10, visualizar)

        else: 
            cap.release()

# Conversion de color
def hsvf():
    global hsv, rgb, gray
    # Colores
    rgb = 0
    hsv = 1
    gray = 0
    detcolor = 0
# RGB
def rgbf():
    global hsv, rgb, gray
    # Colores
    rgb = 1
    hsv = 0
    gray = 0
    detcolor = 0

# GRAY
def grayf():
    global hsv, rgb, gray
    # Colores
    rgb = 0
    hsv = 0
    gray = 1
    detcolor = 0

# Colores
def colores():
    global slider1, slider11, slider2, slider22, slider33, detcolor
    global slival1, slival11, slival2, slival22, slival3, slival33
    # Activamos deteccion de color
    detcolor = 1

    # Extraemos el sliders H
    slival1 = slider1.get()
    slival11 = slider11.get()
    print(slival1, slival11)
    # Extraemos el sliders S
    slival2 = slider2.get()
    slival22 = slider22.get()
    print(slival2, slival22)
    # Extraemos el sliders V
    slival3 = slider3.get()
    slival33 = slider33.get()
    print(slival3, slival33)

    # Deteccion de color
    if detcolor == 1:
        # Deteccion de color
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Establecemos el rango minimo y maximo para la codificacion HSV
        color_oscuro = np.array([slival1, slival2, slival3])
        color_brilla = np.array([slival11, slival22, slival33])

        # Detectamos los pixeles que esten dentro de los rangos
        mascara = cv2.inRange(hsv, color_oscuro, color_brilla)

        # Mascara
        mask = cv2.bitwise_and(frame, frame, mask=mascara)

        mask = imutils.resize(mask, width=360)

        # Convertimos el video
        im2 = Image.fromarray(mask)
        img2 = ImageTk.PhotoImage(image=im2)

        # Mostramos en el GUI
        lblVideo2.configure(image=img2)
        lblVideo2.image = img2
        lblVideo2.after(10, colores)



# Funcion iniciar
def iniciar():
    global cap
    # Elegimos la camara
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    visualizar()
    print("aprende e ingenia youtube")

# Funcion finalizar
def finalizar():
    cap.release()
    cv2.DestroyAllWindows()
    print("FIN")


# Variables
cap = None
hsv = 0
gray = 0
rgb = 1
detcolor = 0


#  Ventana Principal
# Pantalla
pantalla = Tk()
pantalla.title("GUI | TKINTER | VISION ARTIFICIAL | PEPITO PEREZ")
pantalla.geometry("1280x720")  # Asignamos la dimension de la ventana




# Interfaz
texto1 = Label(pantalla, text="VIDEO EN TIEMPO REAL: ")


texto2 = Label(pantalla, text="CONVERSION DE COLOR: ")


texto3 = Label(pantalla, text="DETECCION DE COLOR: ")


# Botones
# Iniciar Video

inicio = Button(pantalla, text="Iniciar", height="40", width="200", command=iniciar)

# Finalizar Video
fin = Button(pantalla, text="Finalizar", height="40", width="200", command=finalizar)


# HSV

bhsv = Button(pantalla, text="HSV", height="40", width="200", command=hsvf)

# RGB
brgb = Button(pantalla, text="RGB", height="40", width="200", command=rgbf)

# GRAY
grayb = Button(pantalla, text="RGB", height="40", width="200", command=grayf)


# Colores
color = Button(pantalla, text="Colores",height="40", width="200", command=colores)


# Sliders
# Color H
slider1 = Scale(pantalla, from_ = 0, to = 179, orient=HORIZONTAL)
slider1.place(x = 80, y = 150)
slider11 = Scale(pantalla, from_ = 0, to = 179, orient=HORIZONTAL)
slider11.place(x = 190, y = 150)
# Color S
slider2 = Scale(pantalla, from_ = 0, to = 255, orient=HORIZONTAL)
slider2.place(x = 80, y = 200)
slider22 = Scale(pantalla, from_ = 0, to = 255, orient=HORIZONTAL)
slider22.place(x = 190, y = 200)
# Color V
slider3 = Scale(pantalla, from_ = 0, to = 255, orient=HORIZONTAL)
slider3.place(x = 80, y = 250)
slider33 = Scale(pantalla, from_ = 0, to = 255, orient=HORIZONTAL)
slider33.place(x = 190, y = 250)



# Video
lblVideo = Label(pantalla)
lblVideo.place(x = 320, y = 50)

lblVideo2 = Label(pantalla)
lblVideo2.place(x = 470, y = 500)

pantalla.mainloop()


