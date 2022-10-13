import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from naoqi import ALProxy

#Hier wird ein Proxy für ALMemory erstellt dass als Schnittstelle
#zwischen Python und Choreograph dient
memProxy = ALProxy("ALMemory", "localhost", 9559)

class ImgProcess():

    def calibration(self):

        #Auswählen der Webcam als VideoCapture-Device.
        cap = cv.VideoCapture(0)

        #Hier wird zunächst ein einzelner Frame mit der Webcam aufgenommen
        #um die nötigen Punkte für die Affine-Transformation zu bestimmen.
        ret, frame = cap.read()
        cap.release()

        #Das Bild wird nun angezeigt. Die entsprechenden Punkte können
        #notiert und in den folgenden Zeilen als Input in den Variablen
        #gespeichert werden
        plt.imshow(frame)
        plt.show()

        ##Die Dimensionen des Frames werden in den entsprechenden
        #Variablen gespeichert.
        rows, cols, ch = frame.shape

        pt1x = int(input('X-Koordinate von Punkt1:'))
        pt1y = int(input('Y-Koordinate von Punkt1:'))
        pt2x = int(input('X-Koordinate von Punkt2:'))
        pt2y = int(input('Y-Koordinate von Punkt2:'))
        pt3x = int(input('X-Koordinate von Punkt3:'))
        pt3y = int(input('Y-Koordinate von Punkt3:'))

        cornerPts1 = np.float32([[pt1x, pt1y], [pt2x, pt2y], [pt3x, pt3y]])
        cornerPts2 = np.float32([[0, 0], [0, 480], [640, 0]])

        #Die Transformationsmatrix aus den entsprechenden Punkten
        #wird erstellt.
        M = cv.getAffineTransform(cornerPts1,cornerPts2)

        #Mit der Transormationsmatrix wird das Bild so verändert,
        #dass es genau vom Schachbrett ausgefüllt wird
        dst = cv.warpAffine(frame,M,(cols,rows))

        #Nun wird das Bild in der korrekten Form dargestellt.
        plt.imshow(dst)
        plt.show()

        #Die Eckpunkte des ROI(Region of Interest) in diesem Fall
        #das obere rechte Feld werden wieder notiert und per Userinput
        #als Variable gespeichert.
        cutPt1 = int(input('X-Koordinate von Schnitt:'))
        cutPt2 = int(input('Y-Koordinate von Schnitt:'))

        #Die relevanten Punkte werden als Rückgabewert der Funktion
        #zurückgegeben.
        return cornerPts1, cornerPts2, cutPt1, cutPt2

    #Die ermittelten Punkte aus calibration() werden hier als Parameter
    #übergeben
    def awaitMove(self,pts1, pts2, cutX, cutY):

        #Hier werden zunächst die gleichen Schritte wie in
        #calibration() ausgeführt
        cap = cv.VideoCapture(0)
        ret, frame = cap.read()
        rows, cols, ch = frame.shape
        M = cv.getAffineTransform(pts1, pts2)
        i = 0
        while cap.isOpened():
            ret, frame = cap.read()

            #Bild wird dem Schachbrett angepasst
            dst = cv.warpAffine(frame, M, (cols, rows))

            #Bild wird in ein Graustufenbild umgewandelt
            gray = cv.cvtColor(dst, cv.COLOR_BGR2GRAY)

            #Graustufenbild wird in ein Schwarz-Weiß Bild umgewandelt,
            #bei den Pixel unter einem Farbwert von 100 schwarz, und
            #Pixel ab einem Wert von 100 weiß gefärbt werden.
            ret, thresh1 = cv.threshold(gray, 100, 255, cv.THRESH_BINARY)

            #roi wird festgelegt
            roi = thresh1[0:cutY, cutX:640]

            #Nach dem ersten Durchgang werden der vorhergegangene Frame
            #mit dem aktuellen Frame verglichen, indem die Differenz der
            #Pixelwerte gebildet wird. Wenn ausreichend viele Pixel
            #verschieden sind um Lichteinflüsse etc. auszuschließen,
            #wird erkannt, dass der König auf dieses Feld gesetzt
            #wurde und die Variable in ALMemory wird entsprechend
            #verändert.

            if i > 0:
                difference = cv.subtract(roi, prev_frame)

                if cv.countNonZero(difference) >= 40:
                    memProxy.insertData("KingMoved", 1)


            prev_frame = roi
            cv.imshow('Frame', roi)
            if cv.waitKey(5000) & 0xFF == ord('q'):
                break

            i += 1
        cap.release()
        cv.destroyAllWindows()



