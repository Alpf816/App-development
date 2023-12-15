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
def nada(x):
    pass


cv2.namedWindow('parametros')
cv2.createTrackbar('Tonalidad minima','parametros',0,255,nada)
cv2.createTrackbar('Tonalidad maxima','parametros',0,255,nada)
cv2.createTrackbar('pureza minima','parametros',0,255,nada)
cv2.createTrackbar('pureza maxima','parametros',0,255,nada)
cv2.createTrackbar('luminosidad minima','parametros',0,255,nada)
cv2.createTrackbar('luminosidad maxima','parametros',0,255,nada)
cv2.createTrackbar('Kernel X','parametros',0,30,nada)
cv2.createTrackbar('Kernel Y','parametros',0,30,nada)        

cap = cv2.VideoCapture(0)
while(1):
    ret, frame = cap.read()
    if ret:
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

        tmin = cv2.getTrackbarPos('Tonalidad minima','parametros')
        tmax = cv2.getTrackbarPos('Tonalidad maxima','parametros')
        pmin = cv2.getTrackbarPos('pureza minima','parametros')
        pmax = cv2.getTrackbarPos('pureza maxima','parametros')
        lmin = cv2.getTrackbarPos('luminosidad minima','parametros')
        lmax = cv2.getTrackbarPos('luminosidad maxima','parametros')
        kernX= cv2.getTrackbarPos('Kernel X','parametros')
        kernY= cv2.getTrackbarPos('Kernel Y','parametros')

        color_oscuro = np.array([tmin,pmin,lmin])
        color_claro = np.array([tmax,pmax,lmax])

        mascara = cv2.inRange(hsv,color_oscuro,color_claro)

        kernel = np.ones((kernX,kernY),np.uint8)

        mascara = cv2.morphologyEx(mascara,cv2.MORPH_CLOSE,kernel)
        mascara = cv2.morphologyEx(mascara,cv2.MORPH_OPEN,kernel)

        contorno, _ = cv2.findContours(mascara,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(frame,contorno,-1,(0,0,0),2)

        cv2.imshow('camara',frame)
        cv2.imshow('Mascara',mascara)
        k = cv2.waitKey(5)
        if k == 27:
            cv2.destroyAllWindows()
cap.release()
        





            
    




#configuracion de (gui)

#botones y sliders





