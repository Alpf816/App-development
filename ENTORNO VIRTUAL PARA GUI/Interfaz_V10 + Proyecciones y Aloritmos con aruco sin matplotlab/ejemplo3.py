import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QGridLayout, QCheckBox, QSlider
from PyQt6.QtCore import QTimer, Qt
import serial

class SerialControlWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Inicialización de la conexión serial, inicialmente no conectado.
        self.ser = None

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Control de Botonera y Potenciómetros")
        self.setGeometry(100, 100, 600, 400)  # Adjusted size to be less wide

        grid_layout = QGridLayout(self)

        # Sliders para los potenciómetros
        self.sliders = {
            'Pot1': QSlider(Qt.Orientation.Horizontal),
            'Pot2': QSlider(Qt.Orientation.Horizontal)
        }
        self.sliders['Pot1'].setRange(0, 1023)
        self.sliders['Pot2'].setRange(0, 1023)
        grid_layout.addWidget(QLabel("Potenciómetro 1"), 0, 0)
        grid_layout.addWidget(self.sliders['Pot1'], 0, 1, 1, 6)  # Span 6 columns
        grid_layout.addWidget(QLabel("Potenciómetro 2"), 1, 0)
        grid_layout.addWidget(self.sliders['Pot2'], 1, 1, 1, 6)  # Span 6 columns

        # Botones para entradas digitales con nombres específicos
        self.buttons = {}
        button_names = [
            ('DI2', 'Borrar Línea\nEje Y'), ('DI3', 'Cambiar Área\nde Superficie'), 
            ('DI4', 'Enviar\nDatos'), ('DI5', 'Precisión'), 
            ('DI6', 'Enviar\nDatos'), ('DI7', 'Cambiar\nEsquina'), 
            ('DI8', 'Línea de Ayuda\nEje Y'), ('DI9', 'Línea de Ayuda\nEje X'), 
            ('DI10', 'Añadir Línea\nEje Y'), ('DI11', 'Borrar Línea\nEje X'), 
            ('DI12', 'Añadir Línea\nEje X')
        ]

        start_row = 3  # Start from the third row
        num_columns = 6
        for i, (key, name) in enumerate(button_names):
            button = QPushButton(name)
            button.setCheckable(True)
            button.clicked.connect(lambda checked, k=key: self.toggle_button(k, checked))
            self.update_button_style(button, 'False')
            self.buttons[key] = button
            # Place button in grid: calculate row and column
            row = start_row + i // num_columns
            col = i % num_columns
            grid_layout.addWidget(button, row, col)

        # Selector para activar/desactivar la conexión serial
        self.serial_switch = QCheckBox("Activar Conexión Serial")
        self.serial_switch.setChecked(False)
        self.serial_switch.toggled.connect(self.toggle_serial_connection)
        grid_layout.addWidget(self.serial_switch, row + 1, 0, 1, num_columns)  # Span across all columns used for buttons

        self.timer = QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_data)

    def toggle_serial_connection(self, checked):
        if checked:
            try:
                self.ser = serial.Serial("COM4", 9600, timeout=1)
                if not self.ser.isOpen():
                    raise Exception("No se pudo abrir el puerto serial.")
                self.timer.start()
                print("Conexión serial activada.")
            except Exception as e:
                print(f"Error al abrir el puerto serial: {e}")
                self.serial_switch.setChecked(False)
        else:
            if self.ser:
                self.ser.close()
            self.timer.stop()
            print("Conexión serial desactivada.")

    def toggle_button(self, key, checked):
        button = self.buttons[key]
        self.update_button_style(button, 'True' if checked else 'False')

    def update_button_style(self, button, value):
        if value == 'True':
            button.setStyleSheet("background-color: green; color: white;")
            button.setText(f"{button.text().split(':')[0]}: Activado")
        else:
            button.setStyleSheet("background-color: red; color: white;")
            button.setText(f"{button.text().split(':')[0]}")

    def update_data(self):
        if self.ser and self.ser.in_waiting > 0:
            data = self.ser.readline().decode('ascii').strip()
            if data:
                #print("Datos recibidos:", data)
                sensors = data.split(',')
                for sensor in sensors:
                    try:
                        key, value = sensor.strip().split(':')
                        if key.startswith('Pot') and key in self.sliders:
                            self.sliders[key].setValue(int(value))
                        elif key in self.buttons:
                            self.update_button_style(self.buttons[key], 'True' if value == '0' else 'False')
                    except ValueError:
                        print(f"Error en el formato de datos recibidos: '{sensor}'")
                        continue
                    except KeyError:
                        print(f"KeyError con clave '{key}'. Posible clave mal formateada o no definida.")
                        continue

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = SerialControlWidget()
    ex.show()
    sys.exit(app.exec())
