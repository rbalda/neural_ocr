import cv2
import numpy as np
import sys
from numpy import *
from pybrain.structure import *
from pybrain.datasets import SupervisedDataSet
from pybrain.utilities import percentError
from pybrain.supervised.trainers import BackpropTrainer
import learning

WINDOW_SIZE = 20
ROWS = 0
COLUMNS = 1
N_INPUT_LAYER = WINDOW_SIZE*WINDOW_SIZE
N_HIDDEN_LAYER = int(N_INPUT_LAYER/5)
OUTPUT_LAYER = 10
input_layer = LinearLayer(N_INPUT_LAYER)
hidden_layer = SigmoidLayer(N_HIDDEN_LAYER)
output_layer = SoftmaxLayer(OUTPUT_LAYER)
net = None




def binarize_and_filter(img):
    out = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    out = cv2.GaussianBlur(out,(3,3),0)
    ret,out = cv2.threshold(out,200,255,cv2.THRESH_BINARY)
    return out


def resize(img):
    out = cv2.resize(img,(WINDOW_SIZE,WINDOW_SIZE),interpolation=cv2.INTER_CUBIC)
    return out

def crop_image(input_img):
    img_height = input_img.shape[ROWS]
    img_width = input_img.shape[COLUMNS]
    tly=None
    tlx=None
    bry=None
    brx = None
    width=None
    height = None

    flag = 0
    """"margen superior"""
    for i in range(0,img_height):
        for j in range(0,img_width):
            if input_img[i][j]==0:
                flag = 1
                tly = i
                break
        if flag == 1:
            flag = 0
            break

    """margen inferior"""
    for i in range(img_height-1,0,-1):
        for j in range(0,img_width):
            if input_img[i][j]==0:
                flag = 1
                bry = i
                break
        if flag == 1:
            flag = 0
            break

    """margen izquierdo"""
    for j in range(0,img_width):
        for i in range(0,img_height-1):
            if input_img[i][j]==0:
                flag=1
                tlx = j
                break
        if flag==1:
            flag = 0
            break


    """margen derecho"""
    for j in range(img_width-1,0,-1):
        for i in range(0,img_height-1):
            if input_img[i,j]==0:
                flag = 1
                brx = j
                break
        if flag==1:
            flag = 0
            break

    width = brx - tlx
    height = bry - tly
    croped = input_img[tly:tly+height,tlx:tlx+width]
    return croped



def generate_pattern(img):
    pixel_array = []
    i = 0
    for x in range(0,WINDOW_SIZE):
        for y in range(0,WINDOW_SIZE):
            if img[x,y]==255:
                pixel_array.append(1)
            else:
                pixel_array.append(0)
    pixel_array = array(pixel_array)
    # pixel_array.dtype = np.uint8
    return pixel_array


def print_patern(x):
    for i in range(0,WINDOW_SIZE*WINDOW_SIZE):
        if i % WINDOW_SIZE == 0:
            print "\n"
        else:
            if x[i] == 1:
                print "x"
            else:
                print "-"


def init_neural_network():
    neural_net = FeedForwardNetwork()
    neural_net.addInputModule(input_layer)
    neural_net.addModule(hidden_layer)
    neural_net.addOutputModule(output_layer)
    connect1 = FullConnection(input_layer,hidden_layer)
    connect2 = FullConnection(hidden_layer,output_layer)
    neural_net.addConnection(connect1)
    neural_net.addConnection(connect2)
    neural_net.sortModules()
    return neural_net





img = cv2.imread("number.png")
# cv2.imshow("normal",img)
img = binarize_and_filter(img)
img = crop_image(img)
img = resize(img)
ablob = generate_pattern(img)
# net = init_neural_network()
training = learning.get_labeled_data('train-images-idx3-ubyte.gz',
                                'train-labels-idx1-ubyte.gz', 'training')
blob = training['x'][9]
print blob.shape
learning.view_image(ablob)
# print net
# print_patern(a)
# cv2.imshow("hello",img)
# cv2.imshow("blob",blob)
# cv2.waitKey()

#binarize_and_filter(img)