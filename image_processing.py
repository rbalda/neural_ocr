import cv2
import numpy as np
import sys
WINDOW_SIZE = 20
ROWS = 0
COLUMNS = 1



def binarize_and_filter(img):
    out = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    out = cv2.GaussianBlur(out,(3,3),0)
    #ret,out = cv2.threshold(out,150,255,cv2.THRESH_BINARY_INV)
    return out


def resize(img):
    out = cv2.resize(img,(WINDOW_SIZE,WINDOW_SIZE),interpolation=cv2.INTER_CUBIC)
    return out

def crop_digits(input_img):
    rows = input_img[ROWS]
    columns = input_img[COLUMNS]
    tly,tlx,bry,brx = 0
    width , height = 0
    suml, sumr = 0
    flag = 0;
    for i in range(1,rows):
        for j in range(1,columns):
            if input_img[i,j]==0:
                flag = 1
                tly = i
                break
        if flag == 1:
            flag = 0
            break









img = cv2.imread("digitrecognition1.jpg")
cv2.imshow("normal",img)
img = binarize_and_filter(img)
img = resize(img)
cv2.imshow("hello",img)
cv2.waitKey()
#binarize_and_filter(img)