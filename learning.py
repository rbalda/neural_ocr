import cv2

__author__ = 'rbalda'
from struct import unpack
import gzip
import matplotlib.pylab as plt
from numpy import zeros, uint8
import pylab
import os.path
import cPickle as pickle

def get_labeled_data(imagefile, labelfile, picklename):
    """
    Read input-vector (image) and target class (label, 0-9) and return
    it as list of tuples.

    :param imagefile:
    :param labelfile:
    :param picklename:
    :rtype : list.
    """
    if os.path.isfile('%s.pickle' % picklename):
        data = pickle.load(open('%s.pickle' % picklename))
    else:
        # Open the images with gzip in read binary mode
        images = gzip.open(imagefile, 'rb')
        labels = gzip.open(labelfile, 'rb')

        # Read the binary data

        # We have to get big endian unsigned int. So we need '>I'

        # Get metadata for images
        images.read(4)  # skip the magic_number
        number_of_images = images.read(4)
        number_of_images = unpack('>I', number_of_images)[0]
        rows = images.read(4)
        rows = unpack('>I', rows)[0]
        cols = images.read(4)
        cols = unpack('>I', cols)[0]

        # Get metadata for labels
        labels.read(4)  # skip the magic_number
        N = labels.read(4)
        N = unpack('>I', N)[0]

        if number_of_images != N:
            raise Exception('The number of labels did not match '
                            'the number of images.')

        # Get the data
        x = zeros((N, rows, cols), dtype=uint8)  # Initialize numpy array
        y = zeros((N, 1), dtype=uint8)  # Initialize numpy array
        for i in range(N):
            if i % 1000 == 0:
                print("i: %i" % i)
            for row in range(rows):
                for col in range(cols):
                    tmp_pixel = images.read(1)  # Just a single byte
                    tmp_pixel = unpack('>B', tmp_pixel)[0]
                    x[i][row][col] = (float(tmp_pixel) / 255)
            tmp_label = labels.read(1)
            y[i] = unpack('>B', tmp_label)[0]
        data = {'x': x, 'y': y, 'rows': rows, 'cols': cols}
        pickle.dump(data, open("%s.pickle" % picklename, "wb"))
    return data


def view_image(image, label=""):
    """
    View a single image.
    :param image:
    :param label:
    """
    print("Label: %s" % label)
    plt.imshow(image,cmap=plt.cm.gray)
    plt.show()