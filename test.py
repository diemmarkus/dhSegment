#!/usr/bin/env python

import tensorflow as tf
from dh_segment.loader import LoadedModel
from tqdm import tqdm
from glob import glob
import numpy as np
import os
import cv2
from imageio import imread, imsave


def convert_image(img):
    # convert & scale an image for imageio output (uint8)
    img = 255 * img
    return img.astype(np.uint8)


if __name__ == '__main__':


    # diem: config
    bp = '../../../basilis/'
    # bp = '../'

    modelnames = ['hw', 'mp', 'im']

    # I/O
    input_files = glob(bp + 'pages/mp/*')

    output_dir = bp + 'results/mp/'
    os.makedirs(output_dir, exist_ok=True)
    
    # Store coordinates of page in a .txt file
    txt_coordinates = ''

    models = list()

    tuple_models = list()  # list of tuples containing (Session, Graph, Model) for each model

    # For each model to be loaded, create a new graph and session. Then load the model.
    for mn in modelnames:
        graph = tf.Graph()
        session = tf.Session(graph=graph)
        with session.as_default(), graph.as_default():  # This is the important line!
            model = LoadedModel(bp + 'model/', mn, predict_mode='filename')
        tuple_models.append((session, graph, model))

    for filename in tqdm(input_files, desc='Processed files'):

        probList = list()
        basename = os.path.basename(filename).split('.')[0]

        if os.path.exists(os.path.join(output_dir, basename + '-probs.png')):
            print(basename + " skipped...")

        # For each image, predict each pixel's label
        for sess, g, model in tuple_models:
            # You need to call 'predict' method in the same Graph and Session 'environment' as you loaded it
            with sess.as_default(), g.as_default():
                #probs = model.predict(filename, prediction_key='probs')
                prediction_outputs = model.predict(filename)
                probs = prediction_outputs['probs'][0]
                original_shape = prediction_outputs['original_shape']
                probs = probs[:, :, 1]  # Take only class '1' (class 0 is the background)
                probList.append(probs)

                probsN = probs / np.max(probs)  # Normalize to be in [0, 1]

                imsave(os.path.join(output_dir, basename + '-' + model.name + '.png'), convert_image(probsN))

        oImg = np.dstack((probList[0], probList[1], probList[2]))  # stacks 3 h x w arrays -> h x w x 3
        oImg = oImg / np.max(oImg)

        imsave(os.path.join(output_dir, basename + '-probs.png'), convert_image(oImg))
                       
