#librerias
import cv2
cap = cv2.VideoCapture(0)

def getContours(img):
    contours, Hierarcy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        print(area)
        if area <=500:
            cv2.drawContours(frame,cnt,-1,(255,0,0),3)
            perimetro = cv2.arcLength(cnt,True)
            aprrox = cv2.approxPolyDP(cnt,0.5*perimetro,True)
            objCorner = len(aprrox)
            x,y,w,h = cv2.boundingRect(aprrox)

            if objCorner == 3:
                objectType = "triangulo"
            elif objCorner == 4:
                aspecto = w/float(h)#
                if aspecto > 0.95 and aspecto < 1.05:
                    objectType = "Cuadrado"
                else:
                    objectType = "Rectangulo"
            elif objCorner > 4:
                objectType = "Circulo"
            else:
                objectType= "None"
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                cv2.putText(frame, objectType,(x+(w//2)-10,y+(h//2)-10),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,0))

while True:
    ret,frame= cap.read()
    imgGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(7,7),1)
    imgCanny = cv2.Canny(imgBlur,50,50)
    getContours(imgCanny)
    cv2.imshow("figuras geometricas stack",frame)
    
    if cv2.waitKey(1) == 27:
        break


