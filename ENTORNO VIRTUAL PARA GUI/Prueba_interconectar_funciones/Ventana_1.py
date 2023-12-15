from PyQt6 import QtCore, QtGui, QtWidgets 

class Contenedor(QtWidgets.QWidget):
    def __init__(self, window, parent=None):
        super(Contenedor, self).__init__(parent)
        QtCore.Qt.WindowType.FramelessWindowHint
        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(window)
        lay.setContentsMargins(10,10,10,10)



class CInicial(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(CInicial, self).__init__(parent)
        

        # test
        self.setCentralWidget(QtWidgets.QTextEdit())

def crear_ventana():
    inicial = CInicial()
    contenedor =Contenedor(inicial)
    contenedor.resize(640, 480)
    return contenedor, inicial

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication([])
    w = CInicial()
    contenedor = Contenedor(w)
    contenedor.resize(640,480)
    contenedor.show()
    sys.exit(app.exec())