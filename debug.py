#!/usr/bin/env python

from glob import glob
import numpy as np
import os
import cv2
from dh_segment.post_processing.utils import imgInfo, normalize
from dh_segment.post_processing.binarization import threshold, bwClean
from dh_segment.post_processing.detect_elements import findSeparators, findPages
from dh_segment.post_processing.PAGE import Border, Page
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
    pgRects = findPages(pg, seps)


    # show separators
    plt.imshow(img)

    sxy = img.shape[0]/prob.shape[0]

    for s in seps:
        s.scale(sxy)
        l = s.lineCoords()
        plt.plot(l[0], l[1])

    for p in pgRects:
        p.scale(sxy)
        plt.plot(p.pts[:,0], p.pts[:,1])

    # border = [Border.from_array(coords=b, id='border_{}'.format(i)) for i, b in enumerate(pgRects))]

    borders = list()

    for i, p in enumerate(pgRects):
        # borders.append(Border(coords=p, id='border_{}'.format(i)))
        borders.append(Border(coords=p.toPointList()))
        
    pageXml = Page(page_borders = borders)
    pageXml.write_to_file(os.path.join(outDir, 'page.xml'))

    # TODO: add image dimensions!! & filename

    print("tutu")
