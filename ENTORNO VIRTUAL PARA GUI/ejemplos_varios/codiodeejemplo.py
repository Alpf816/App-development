import sys
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget
import cv2

class VideoApp(QMainWindow):
    def __init__(self, parent=None):
        super(VideoApp, self).__init__(parent)
        self.setWindowTitle("Video App")

        self.video_source = 0
        self.vid = cv2.VideoCapture(self.video_source)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.video_label = QLabel(self)
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout = QVBoxLayout(self.central_widget)
        self.layout.addWidget(self.video_label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(10)  # Actualiza cada 10 milisegundos

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            image = QImage(frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(image)

            # Agregar márgenes (20 píxeles)
            margin = 20
            pixmap = pixmap.scaled(self.width() - margin, self.height() - margin, Qt.AspectRatioMode.KeepAspectRatio)

            self.video_label.setPixmap(pixmap)

    def closeEvent(self, event):
        if self.vid.isOpened():
            self.vid.release()
        event.accept()

def main():
    app = QApplication(sys.argv)
    window = VideoApp()
    window.setGeometry(100, 100, 600, 400)  # Establecer la geometría de la ventana
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
