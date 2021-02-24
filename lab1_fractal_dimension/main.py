import cv2
import numpy as np

def get_resolution(img):
    print("{:d}x{:d}".format(img.shape[0], img.shape[1]))

def resize(path, w, h):
    img = cv2.imread(path)
    resized_img = cv2.resize(img, (w, h), cv2.INTER_NEAREST)
    cv2.imwrite('resized_{}'.format(path.rsplit('/')[0]), resized_img)

def grayscale_img(path):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    cv2.imshow(path, img)
    cv2.waitKey(0)
    cv2.imwrite(path, img)

def fractal_dimension(img):
    img_bw = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)[1] / 255
    
    min_dimension = min(img_bw.shape[0], img_bw.shape[1])
    greatest_power = 2 ** np.floor(np.log(min_dimension) / np.log(2))
    exponent = int(np.log(greatest_power) / np.log(2))

    scales = 2 ** np.arange(exponent, 1, -1)

    N = []
    for scale in scales:
        boxes = np.add.reduceat(np.add.reduceat(img_bw, np.arange(0, img_bw.shape[0], scale), axis=0), 
                                np.arange(0, img_bw.shape[1], scale), axis=1)
        non_empty_boxes_number = len(np.where((boxes > 0) & (boxes < scale*scale))[0])
        N.append(non_empty_boxes_number)

    coeffs = np.polyfit(np.log(1/scales), np.log(N), 1)
    return coeffs[0]

paths = ["../koch.png", "../sierpinski.png", "../bricks1.png"]

for path in paths:
    img = cv2.imread(path)
    res = fractal_dimension(img)
    print("{:20}: {}".format(path, res))