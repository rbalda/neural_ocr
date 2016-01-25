from pybrain.datasets import ClassificationDataSet
from pybrain.supervised import BackpropTrainer
from pybrain.utilities import percentError
import learning
import cv2
from image_processing import *

__author__ = 'rbalda'
from pybrain.structure import *

from image_processing import WINDOW_SIZE,OUTPUT_LAYER
import cPickle as pickle


N_INPUT_LAYER = WINDOW_SIZE * WINDOW_SIZE
N_HIDDEN_LAYER = int(N_INPUT_LAYER/2)
input_layer = LinearLayer(N_INPUT_LAYER)
hidden_layer = SigmoidLayer(N_HIDDEN_LAYER)
output_layer = SoftmaxLayer(OUTPUT_LAYER)
OUTPUT_LAYER = 10
MOMENTUM = 0.1
L_RATE = 0.01
L_DECAY = 1
W_DECAY = 0.01
EPOCHS = 20
net = None


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




def training_and_testing():
    nn= init_neural_network()

    training = learning.get_labeled_data('train-images-idx3-ubyte.gz',
                                'train-labels-idx1-ubyte.gz','trainig')
    test = learning.get_labeled_data('t10k-images-idx3-ubyte.gz',
                                 't10k-labels-idx1-ubyte.gz','test')

    FEATURES = N_INPUT_LAYER
    print("Caracteristicas a analizar: %i"%FEATURES)
    testdata = ClassificationDataSet(FEATURES,1,nb_classes=OUTPUT_LAYER)
    trainingdata = ClassificationDataSet(FEATURES,1,nb_classes=OUTPUT_LAYER)


    for i in range(len(test['data'])):
        testdata.addSample(test['data'][i],test['label'][i])
    for j in range(len(training['data'])):
        trainingdata.addSample(training['data'][j],training['label'][j])

    trainingdata._convertToOneOfMany()
    testdata._convertToOneOfMany()

    trainer = BackpropTrainer(nn,dataset=trainingdata,momentum=MOMENTUM,verbose=True,
                         weightdecay=W_DECAY,learningrate=L_RATE,lrdecay=L_DECAY)

    for i in range(EPOCHS):
        trainer.trainEpochs(1)
        trnresult = percentError(trainer.testOnClassData(),
                                 trainingdata['class'])
        tstresult = percentError(trainer.testOnClassData(
                                 dataset=testdata), testdata['class'])

        print("epoch: %4d" % trainer.totalepochs,
                     "  train error: %5.2f%%" % trnresult,
                     "  test error: %5.2f%%" % tstresult)
    return nn


def save_network(nn):
    file = open('network_data.pickle','w')
    pickle.dump(nn,file)
    file.close()


def generate_network_from_file(name):
    file = open(name,'r')
    nn = pickle.load(file)
    return nn


if __name__=='__main__':
    # nn = training_and_testing()
    # save_network(nn)
    nn = generate_network_from_file('network_data.pickle')
    img = cv2.imread('10.png')
    img2 = img
    img = binarize_and_filter(img)
    imgR = crop_image(img)
    imgR1 = resize(imgR)
    cv2.imshow("7 normalizado",imgR1)
    cv2.imshow("7 normal",img2)
    X = generate_pattern(imgR1)
    predict = nn.activate(X)
    nn.activate(X)
    p = argmax(predict,axis=0)
    print p
    cv2.waitKey()