import cv2
import numpy as np
from PyQt6.QtWidgets import QApplication, QLabel, QSlider, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap

def adjust_brightness_contrast(image, brightness=0, contrast=0):
    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow) / 255
        gamma_b = shadow

        buf = cv2.addWeighted(image, alpha_b, image, 0, gamma_b)
    else:
        buf = image.copy()

    if contrast != 0:
        f = 131 * (contrast + 127) / (127 * (131 - contrast))
        alpha_c = f
        gamma_c = 127 * (1 - f)

        buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)

    return buf

def invert_image(image):
    return cv2.bitwise_not(image)

class ArUcoDetectionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.brightness = 0
        self.contrast = 0

        self.cap = cv2.VideoCapture(0)
        self.timer = self.startTimer(30)

        self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        self.parameters = cv2.aruco.DetectorParameters()
        self.camera_matrix = np.array([[467.91, 0, 314.081],
                                       [0, 467.91, 247.2],
                                       [0, 0, 1]], dtype=float)
        self.dist_coeffs = np.array([0.078, -0.197, 0.0004, 0], dtype=float)

    def initUI(self):
        self.setWindowTitle('ArUco Detection')

        self.image_label = QLabel(self)
        self.brightness_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.brightness_slider.setRange(-100, 100)
        self.brightness_slider.valueChanged.connect(self.on_brightness_change)

        self.contrast_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.contrast_slider.setRange(-100, 100)
        self.contrast_slider.valueChanged.connect(self.on_contrast_change)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.brightness_slider)
        layout.addWidget(self.contrast_slider)
        self.setLayout(layout)

    def on_brightness_change(self, value):
        self.brightness = value
        self.update_image()

    def on_contrast_change(self, value):
        self.contrast = value
        self.update_image()

    def timerEvent(self, event):
        self.update_image()

    def update_image(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        adjusted = adjust_brightness_contrast(gray, self.brightness, self.contrast)

        corners, ids, rejected = cv2.aruco.detectMarkers(adjusted, self.aruco_dict, parameters=self.parameters)

        if ids is not None:
            for i in range(len(ids)):
                rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners[i], 0.05, self.camera_matrix, self.dist_coeffs)
                cv2.aruco.drawDetectedMarkers(adjusted, corners)
                cv2.drawFrameAxes(adjusted, self.camera_matrix, self.dist_coeffs, rvecs[0], tvecs[0], 0.1)

        qimg = QImage(adjusted.data, adjusted.shape[1], adjusted.shape[0], QImage.Format.Format_Grayscale8)
        pixmap = QPixmap.fromImage(qimg)
        self.image_label.setPixmap(pixmap)

if __name__ == '__main__':
    app = QApplication([])
    window = ArUcoDetectionApp()
    window.show()
    app.exec()
