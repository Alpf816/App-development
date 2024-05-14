import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QWidget, QPushButton
from PyQt6.QtCore import QTimer
import serial

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        try:
            self.ser = serial.Serial("COM4", 9600, timeout=1)
            if not self.ser.isOpen():
                raise Exception("No se pudo abrir el puerto serial.")
        except Exception as e:
            print(f"Error al abrir el puerto serial: {e}")
            exit()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Lectura de Sensores con Arduino")
        self.setGeometry(100, 100, 600, 400)
        
        self.layout = QVBoxLayout()
        self.labels = {}
        self.buttons = {}

        # Etiquetas para los potenciómetros
        self.labels['Pot1'] = QLabel("Potenciómetro 1: Esperando datos...")
        self.labels['Pot2'] = QLabel("Potenciómetro 2: Esperando datos...")
        self.layout.addWidget(self.labels['Pot1'])
        self.layout.addWidget(self.labels['Pot2'])

        # Crear botones para entradas digitales con nombres específicos
        button_names = {
            'DI2': 'Borrar Línea Eje Y',
            'DI3': 'Cambiar Área de Superficie',
            'DI4': 'Enviar Datos',
            'DI5': 'Precisión',
            'DI6': 'Enviar Datos',
            'DI7': 'Cambiar Esquina',
            'DI8': 'Línea de Ayuda Eje Y',
            'DI9': 'Línea de Ayuda Eje X',
            'DI10': 'Añadir Línea Eje Y',
            'DI11': 'Borrar Línea Eje X',
            'DI12': 'Añadir Línea Eje X'
        }

        for key, name in button_names.items():
            self.buttons[key] = QPushButton(name)
            self.buttons[key].setEnabled(False)  # Desactivar para que no sean clickeables
            self.update_button_style(self.buttons[key], 'False')  # Inicializar con estilo de 'False'
            self.layout.addWidget(self.buttons[key])

        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)
        
        # Temporizador para actualizar los datos cada 100 ms
        self.timer = QTimer(self)
        self.timer.setInterval(100)  # en milisegundos
        self.timer.timeout.connect(self.update_data)
        self.timer.start()

    def update_button_style(self, button, value):
        base_text = button.text().split(":")[0]  # Remover cualquier estado previo
        if value == 'True':
            button.setStyleSheet("background-color: green; color: white;")
            button.setText(f"{base_text}: Activado")
        else:
            button.setStyleSheet("background-color: red; color: white;")
            button.setText(f"{base_text}: Desactivado")

    def update_data(self):
        if self.ser.in_waiting > 0:
            data = self.ser.readline().decode('ascii').strip()
            if data:
                print("Datos recibidos:", data)
                sensors = data.split(',')
                for sensor in sensors:
                    try:
                        key, value = sensor.strip().split(':')
                        if key in self.labels:
                            self.labels[key].setText(f"{key}: {value}")
                        elif key in self.buttons:
                            self.update_button_style(self.buttons[key], 'True' if value == '0' else 'False')
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
