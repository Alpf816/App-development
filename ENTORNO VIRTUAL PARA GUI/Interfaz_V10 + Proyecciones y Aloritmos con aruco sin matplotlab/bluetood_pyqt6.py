import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QWidget
from PyQt6.QtCore import QTimer
import serial

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ser = serial.Serial("COM4", 9600, timeout=1)
        if self.ser.isOpen():
            print("Conexión serial establecida correctamente.")
        else:
            print("No se pudo establecer la conexión serial.")
            exit()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Lectura de Sensores con Arduino")
        self.setGeometry(100, 100, 400, 300)
        
        self.layout = QVBoxLayout()
        self.labels = {}

        # Crear etiquetas para los potenciómetros
        self.labels['Pot1'] = QLabel("Potenciómetro 1: Esperando datos...")
        self.labels['Pot2'] = QLabel("Potenciómetro 2: Esperando datos...")
        self.layout.addWidget(self.labels['Pot1'])
        self.layout.addWidget(self.labels['Pot2'])

        # Crear etiquetas para entradas digitales
        for i in range(2, 14):
            self.labels[f'DI{i}'] = QLabel(f"DI{i}: Esperando datos...")
            self.layout.addWidget(self.labels[f'DI{i}'])

        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)
        
        # Temporizador para actualizar los datos cada 100 ms
        self.timer = QTimer(self)
        self.timer.setInterval(100)  # en milisegundos
        self.timer.timeout.connect(self.update_data)
        self.timer.start()

    def update_data(self):
        if self.ser.inWaiting() > 0:
            data = self.ser.readline().decode('ascii').strip()
            if data:
                print("Datos recibidos:", data)
                sensors = data.split(',')
                for sensor in sensors:
                    try:
                        key, value = sensor.strip().split(':')  # Asegurar la eliminación de espacios extras
                        # Comprobamos si la clave es válida
                        if key in self.labels:
                            if 'DI' in key:
                                value = 'True' if value == '0' else 'False'
                            self.labels[key].setText(f"{key}: {value}")
                        else:
                            print(f"Clave no reconocida o no esperada: '{key}'")
                    except ValueError:
                        print(f"Error en el formato de datos recibidos: '{sensor}'")
                        continue
                    except KeyError:
                        print(f"KeyError con clave '{key}'. Posible clave mal formateada o no definida.")
                        continue


    def closeEvent(self, event):
        self.ser.close()
        print("Conexión serial cerrada.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
