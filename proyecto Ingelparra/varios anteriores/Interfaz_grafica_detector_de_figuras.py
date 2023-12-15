#librerias g
import cv2
from tkinter import *
from tkinter import messagebox

#configuracion de (gui)
root = Tk()

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

root.mainloop()
