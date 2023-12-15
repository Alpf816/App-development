import cv2

capture = cv2.VideoCapture("http://192.168.11.10:8080/video")}

while(True):
    _, frame = capture.read()
    cv2.imshow('videoc',frame)
    if cv2.waitKey(1)== ord("q"):
        break
capture.release()
cv2.destroyAllWindows