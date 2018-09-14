#!/usr/bin/env python

import tensorflow as tf
from dh_segment.loader import LoadedModel
from tqdm import tqdm
from glob import glob
import numpy as np
import os
import cv2
from imageio import imread, imsave
from sacred import Experiment

ex = Experiment('dhSegment_test')

@ex.config
def default_config():
    modelDir   = None          # Directory with model data
    modelName = 'ps'          # the name of your model (or its folder name)
    testDir    = None          # test directory
    outDir     = None          # output directory
    gpu = ''                    # GPU to be used

def convert_image(img):
    # convert & scale an image for imageio output (uint8)
    img = 255 * img
    return img.astype(np.uint8)


@ex.automain
def run(testDir, modelDir, modelName, outDir, _config):

    # Create output directory
    os.makedirs(outDir, exist_ok=True)

    # I/O
    files = glob(testDir + '/*')

    # Store coordinates of page in a .txt file
    txt_coordinates = ''

    models = list()

    with tf.Session():  # Start a tensorflow session
        # Load the model
        model = LoadedModel(modelDir, modelName, predict_mode='filename')

        for filename in tqdm(files, desc='Processed files'):

            basename = os.path.basename(filename).split('.')[0]

            if os.path.exists(os.path.join(outDir, basename + '-probs.png')):
                print(basename + " skipped...")

            prediction_outputs = model.predict(filename)
            probs = prediction_outputs['probs'][0]
            original_shape = prediction_outputs['original_shape']
            # Take only class '1' (class 0 is the background)
            probs = probs[:, :, 1]

            # probsN = probs / np.max(probs)  # Normalize to be in [0, 1]

            imsave(os.path.join(outDir, basename + '-' +
                   model.name + '.png'), convert_image(probs))
