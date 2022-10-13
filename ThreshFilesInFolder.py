import cv2 as cv
import os
from matplotlib import pyplot as plt
import imghdr

path = os.path.join('D:', 'Tensorflow Object Detection', 'TFODCourse', 'Tensorflow', 'workspace', 'images', 'convert')

for file in os.listdir(path):
    img_path = os.path.join(path, file)
    if imghdr.what(img_path) == 'jpeg':
        img = cv.imread(img_path)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        ret,thresh1 = cv.threshold(gray,100,255,cv.THRESH_BINARY)
        cv.imwrite(img_path, thresh1)