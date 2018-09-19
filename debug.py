#!/usr/bin/env python

from glob import glob
import numpy as np
import os
import cv2
from dh_segment.post_processing.utils import imgInfo, normalize
from dh_segment.post_processing.binarization import threshold, bwClean
from dh_segment.post_processing.detect_elements import findSeparators, findPages
from imageio import imread, imsave
from sacred import Experiment
import matplotlib.pyplot as plt

ex = Experiment('dhSegment_test')

@ex.config
def default_config():
    imgPath   = None          # test image path
    probPath  = None          # corresponding probability image
    outDir    = None          # output directory

@ex.automain
def run(imgPath, probPath, outDir, _config):

    # Create output directory
    os.makedirs(outDir, exist_ok=True)

    img = imread(imgPath)
    prob = imread(probPath)

    imgInfo(prob, "probs-before")

    prob = prob.astype(float)
    prob = prob / np.max(prob)

    # find separators
    sepP = prob[:,:,2]
    seps = findSeparators(sepP)

    # find page
    pg = prob[:,:,1]
    


    # show separators
    plt.imshow(img)

    for s in seps:
        s.scale(img.shape[0]/prob.shape[0])
        plt.plot(s.line()[1], s.line()[0])

    print("tutu")
