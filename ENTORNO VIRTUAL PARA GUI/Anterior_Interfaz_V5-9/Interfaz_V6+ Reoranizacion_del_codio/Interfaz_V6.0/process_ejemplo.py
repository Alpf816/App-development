import cv2
import multiprocessing
import time

class VideoProcess(multiprocessing.Process):
    def __init__(self, input_queue, output_signal):
        super().__init__()
        self.input_queue = input_queue
        self.output_signal = output_signal
        print("init process")
    def run(self):
        print("Inicio process")
        try:
            while True:
                if not self.input_queue.empty():
                    frame = self.input_queue.get()
                    # Aquí puedes realizar el procesamiento de la imagen con OpenCV
                    # Por ejemplo, podrías convertir la imagen a escala de grises
                    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                    # Emitir la señal con el frame procesado
                    self.output_signal.put(gray_frame)
                    time.sleep(0.02)
        except Exception as e:
            print(f"Error en VideoProcess: {e}")

