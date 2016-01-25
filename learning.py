import os
import cv2
import cPickle as pickle


__author__ = 'rbalda'
from image_processing import crop_image, invert_color,resize, apply_threshold, generate_pattern
from struct import unpack
import gzip
import matplotlib.pylab as plt
from numpy import zeros, uint8


def get_labeled_data(imagefile, labelfile,database):
    """Read input-vector (image) and target class (label, 0-9) and return
       it as list of tuples.
    """
    if os.path.isfile('%s.pickle' % database):
        data = pickle.load(open('%s.pickle' % database))
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
        x = zeros((rows, cols), dtype=uint8)  # Initialize numpy array
        y = zeros((N, 1), dtype=uint8)  # Initialize numpy array

        w = zeros((N,400),dtype=uint8)
        for i in range(N):
            if i % 1000 == 0:
                print("i: %i" % i)
            for row in range(rows):
                for col in range(cols):
                    tmp_pixel = images.read(1)  # Just a single byte
                    tmp_pixel = unpack('>B', tmp_pixel)[0]
                    x[row][col] = (tmp_pixel)
            z = resize(crop_image(invert_color(apply_threshold(x))))
            w[i] = generate_pattern(z)
            x = zeros((rows, cols), dtype=uint8)
            tmp_label = labels.read(1)
            y[i]=unpack('>B',tmp_label)[0]
        data = {'data': w, 'label': y}
        pickle.dump(data, open("%s.pickle" % database, "wb"))
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