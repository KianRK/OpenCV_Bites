import cv2 as cv
import os
from matplotlib import pyplot as plt
import imghdr

#With this code you can apply a black and white transformation to all jpeg files in a specified folder.
#You just have to adjust the arguments in os.path.join() and after you run the programm.. et voila - every jpeg file in the folder will
#be a black and white image.
#It works by first transforming the image to a grayscale image, which basically means reducing the colorchannels from 3 (for R(ed), G(reen) and B(lue)) to 1, so that each pixel
#is left with a single value between 0 and 255. This is necessary because cv.threshold-method expects a grayscale image as an argument.
#The cv.threshold() then changes the value of each pixel to either 0 or 255 according to the value in the limit variable 
#(0/black for a value <= limit and 255/white for a value > limit). The value of 255 can also be changed, depending of the brightness you want your images to have.
#after transforming your image, your old image file gets overwritten, so if you want to keep it, you have to define a new path for the transformed image and pass it as an
#argument to cv.imwrite().

path = os.path.join('D:', 'dir1', 'dir2', 'dir3')

limit = 100

for file in os.listdir(path):
    img_path = os.path.join(path, file)
    if imghdr.what(img_path) == 'jpeg':
        img = cv.imread(img_path)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        ret,thresh1 = cv.threshold(gray,limit,255,cv.THRESH_BINARY)
        cv.imwrite(img_path, thresh1)
