import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class ChecklistWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        # Configuración inicial de la ventana
        self.setWindowTitle("Checklist de Condiciones")
        self.resize(200, 150)
        
        # Fuente para los íconos
        font = QFont("Arial", 8)
        
        # Layout principal
        layout = QVBoxLayout()
        
        # Condiciones y sus estados (True significa activo y por ende chulo, False es una cruz)
        condiciones = {
            "Condición 1": True,
            "Condición 2": False,
            "Condición 3": True,
            "Condición 4": False
        }
        
        # Creamos un QLabel para cada condición
        for condicion, estado in condiciones.items():
            label = QLabel()
            label.setFont(font)
            label.setText(f"{condicion}: {'✓' if estado else '✗'}")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(label)
        
        self.setLayout(layout)

# Función principal que ejecuta la aplicación
def main():
    app = QApplication(sys.argv)
    checklist = ChecklistWidget()
    checklist.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
