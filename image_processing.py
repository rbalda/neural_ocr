import cv2
import numpy as np

def binarize_and_filter(img):
    out = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    out = cv2.GaussianBlur(out,(3,3),0)
    #ret,out = cv2.threshold(out,150,255,cv2.THRESH_BINARY_INV)
    return out



#def crop_image(image):

img = cv2.imread("digitrecognition1.jpg")
cv2.imshow("normal",img)
img = binarize_and_filter(img)
cv2.imshow("hello",img)
cv2.waitKey()
#binarize_and_filter(img)