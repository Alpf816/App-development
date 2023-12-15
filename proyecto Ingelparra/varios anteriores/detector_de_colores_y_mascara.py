#Librerias
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from PIL import Image
from PIL import ImageTk
import cv2
import numpy as np
import imutils
from tkinter import messagebox

#configuracion botones

def video_de_entrada():
    global cap
    cap = cv2.VideoCapture(0)  
    ret, frame = cap.read()
    if ret:
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

        tmin = sl1.get()
        tmax = sl2.get()
        pmin = sl3.get()
        pmax = sl4.get()
        lmin = sl5.get()
        lmax = sl6.get()
        kernX= sl7.get()
        kernY= sl8.get()

        color_oscuro = np.array([tmin,pmin,lmin])
        color_claro = np.array([tmax,pmax,lmax])

        mascara = cv2.inRange(hsv,color_oscuro,color_claro)

        kernel = np.ones((kernX,kernY),np.uint8)

        mascara = cv2.morphologyEx(mascara,cv2.MORPH_CLOSE,kernel)
        mascara = cv2.morphologyEx(mascara,cv2.MORPH_OPEN,kernel)

        contorno, _ = cv2.findContours(mascara,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(frame,contorno,-1,(0,0,0),2)

        cv2.imshow("camara",frame)
        cv2.imshow("Mascara",mascara)
        





            
    
def finalizar():
    global cap
    cap.release()
cap = None



#configuracion de (gui)
root = Tk()
root.title("interfaz de pruebas")

menuBar = Menu(root)
root.config(menu = menuBar)

archivoMenu = Menu(menuBar, tearoff=0)

archivoMenu.add_command(label="Nuevo")
archivoMenu.add_command(label="Abrir")
archivoMenu.add_command(label="Guardar")
archivoMenu.add_command(label="Cerrar")
archivoMenu.add_separator
archivoMenu.add_command(label="Salir", command= root.quit)

editMenu = Menu(menuBar, tearoff=0)

editMenu.add_command(label="cortar")

ayudaMenu = Menu(menuBar, tearoff=0)
ayudaMenu.add_command(label="ayuda")

menuBar.add_cascade(label="Archivo",menu=archivoMenu)
menuBar.add_cascade(label="Editar",menu=editMenu)
menuBar.add_cascade(label="Ayuda",menu=ayudaMenu)
#pestañas
notebook = ttk.Notebook(root)
pes0 = ttk.Frame(notebook)
pes1 = ttk.Frame(notebook)
notebook.add(pes0,text="parametros")
notebook.add(pes1,text="video")
notebook.pack()

#botones y sliders

btnIniciar = Button(pes1,text="Video en vivo",command=video_de_entrada)
btnIniciar.grid(column=0,row=0)

btnEnd = Button(pes1,text="Finalizar y limpiar",command=finalizar)
btnEnd.grid(column=1,row=0,columnspan=2, pady=10)

lbVideo = Label(pes1)
lbVideo.grid(column=0,columnspan=2)

sl1 = Scale(pes0,from_=0,to=255,orient=HORIZONTAL)
sl1.set(0)
t1 = Label(pes0,text="Tonalidad Minima")
t1.grid(column=3,row=0)
sl1.grid(column=3,row=1)

sl2 = Scale(pes0,from_=0,to=255,orient=HORIZONTAL)
sl2.set(0)
t2 = Label(pes0,text="Tonalidad Maxima")
t2.grid(column=3,row=2)
sl2.grid(column=3,row=3)

sl3 = Scale(pes0,from_=0,to=255,orient=HORIZONTAL)
sl3.set(0)
t3 = Label(pes0,text="Pureza Minima")
t3.grid(column=3,row=4)
sl3.grid(column=3,row=5)

sl4 = Scale(pes0,from_=0,to=255,orient=HORIZONTAL)
sl4.set(0)
t4 = Label(pes0,text="Pureza maxima")
t4.grid(column=3,row=6)
sl4.grid(column=3,row=7)

sl5 = Scale(pes0,from_=0,to=255,orient=HORIZONTAL)
sl5.set(0)
t5 = Label(pes0,text="Luminosidad minima")
t5.grid(column=4,row=0)
sl5.grid(column=4,row=1)

sl6 = Scale(pes0,from_=0,to=255,orient=HORIZONTAL)
sl6.set(0)
t6 = Label(pes0,text="Luminosidad maxima")
t6.grid(column=4,row=2)
sl6.grid(column=4,row=3)

sl7 = Scale(pes0,from_=0,to=255,orient=HORIZONTAL)
sl7.set(0)
t7 = Label(pes0,text="kernel X")
t7.grid(column=4,row=4)
sl7.grid(column=4,row=5)

sl8 = Scale(pes0,from_=0,to=255,orient=HORIZONTAL)
sl8.set(0)
t8 = Label(pes0,text="kernel Y")
t8.grid(column=4,row=6)
sl8.grid(column=4,row=7)

root.mainloop()

cap = cv2.VideoCapture(0)  
while(1):
    ret, frame = cap.read()
    if ret:
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

        tmin = sl1.get()
        tmax = sl2.get()
        pmin = sl3.get()
        pmax = sl4.get()
        lmin = sl5.get()
        lmax = sl6.get()
        kernX= sl7.get()
        kernY= sl8.get()

        color_oscuro = np.array([tmin,pmin,lmin])
        color_claro = np.array([tmax,pmax,lmax])

        mascara = cv2.inRange(hsv,color_oscuro,color_claro)

        kernel = np.ones((kernX,kernY),np.uint8)

        mascara = cv2.morphologyEx(mascara,cv2.MORPH_CLOSE,kernel)
        mascara = cv2.morphologyEx(mascara,cv2.MORPH_OPEN,kernel)

        contorno, _ = cv2.findContours(mascara,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(frame,contorno,-1,(0,0,0),2)

        cv2.imshow("camara",frame)
        cv2.imshow("Mascara",mascara)