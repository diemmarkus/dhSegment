#!/usr/bin/env python

import os
from glob import glob

import cv2
import numpy as np
import tensorflow as tf
from imageio import imread, imsave
from tqdm import tqdm

from dh_segment.io import PAGE
from dh_segment.inference import LoadedModel
from sacred import Experiment

# To output results in PAGE XML format (http://www.primaresearch.org/schema/PAGE/gts/pagecontent/2013-07-15/)
PAGE_XML_DIR = './page_xml'


ex = Experiment('dhSegment_test')


@ex.config
def default_config():
    modelDir = None     # Directory with model data
    testDir = None      # test directory
    outDir = None       # output directory
    gpu = ''            # GPU to be used


def convert_image(img):
    # convert & scale an image for imageio output (uint8)
    img = 255 * img
    return img.astype(np.uint8)


import subprocess as sp
import os


def mask_unused_gpus(num_gpus=1):
    ACCEPTABLE_AVAILABLE_MEMORY = 1024
    COMMAND = "nvidia-smi --query-gpu=memory.free --format=csv"

    try:
        def _output_to_list(x): return x.decode('ascii').split('\n')[:-1]
        memory_free_info = _output_to_list(sp.check_output(COMMAND.split()))[1:]
        memory_free_values = [int(x.split()[0])
                                for i, x in enumerate(memory_free_info)]
        available_gpus = [i for i, x in enumerate(
            memory_free_values) if x > ACCEPTABLE_AVAILABLE_MEMORY]

        if len(available_gpus) < num_gpus:
            raise ValueError('Found only %d usable GPUs in the system' %
                                len(available_gpus))

        aGpus = ','.join(str(x) for x in available_gpus[:num_gpus-1])
        print("using GPU " + aGpus)
        os.environ["CUDA_VISIBLE_DEVICES"] = aGpus

    except Exception as e:
        print('"nvidia-smi" is probably not installed. GPUs are not masked', e)


@ex.automain
def run(testDir, modelDir, outDir, gpu, _config):

    # Create output directory
    os.makedirs(outDir, exist_ok=True)

    # I/O
    files = glob(testDir + '/*')

    # Store coordinates of page in a .txt file
    txt_coordinates = ''

    models = list()
    mask_unused_gpus(2)

    with tf.Session():  # Start a tensorflow session

        # Load the model
        # model = LoadedModel(modelDir, modelName, predict_mode='filename')
        model = LoadedModel(modelDir, predict_mode='filename')

        for filename in tqdm(files, desc='Processed files'):

            basename = os.path.basename(filename).split('.')[0]

            if os.path.exists(os.path.join(outDir, basename + '.xml')):
                print(basename + " skipped...")


            # print("predict filename:" + filename)
            prediction_outputs = model.predict(filename)

            probs = prediction_outputs['probs'][0]
            probs = probs.astype(float)
            # probs = probs / np.max(probs)

            imgPath = os.path.join(testDir, filename)

            # print("loading:" + imgPath)
            img = imread(filename)

            # pageSeparatorsToXml(probs, img.shape, filename, outDir)

            probsN = probs / np.max(probs)  # Normalize to be in [0, 1]

            imsave(os.path.join(outDir, basename + '-articles.png'), convert_image(probs))

    # # If the model has been trained load the model, otherwise use the given model
    # model_dir = 'demo/page_model/export'
    # if not os.path.exists(model_dir):
    #     model_dir = 'demo/model/'

    # input_files = glob('demo/pages/test_a1/images/*')

    # output_dir = 'demo/processed_images'
    # os.makedirs(output_dir, exist_ok=True)
    # # PAGE XML format output
    # output_pagexml_dir = os.path.join(output_dir, PAGE_XML_DIR)
    # os.makedirs(output_pagexml_dir, exist_ok=True)

    # # Store coordinates of page in a .txt file
    # txt_coordinates = ''

    # with tf.Session():  # Start a tensorflow session
    #     # Load the model
    #     m = LoadedModel(model_dir, predict_mode='filename')

    #     for filename in tqdm(input_files, desc='Processed files'):
    #         # For each image, predict each pixel's label
    #         prediction_outputs = m.predict(filename)
    #         probs = prediction_outputs['probs'][0]
    #         original_shape = prediction_outputs['original_shape']
    #         probs = probs[:, :, 1]  # Take only class '1' (class 0 is the background, class 1 is the page)
    #         probs = probs / np.max(probs)  # Normalize to be in [0, 1]

    #         # Binarize the predictions
    #         page_bin = page_make_binary_mask(probs)

    #         # Upscale to have full resolution image (cv2 uses (w,h) and not (h,w) for giving shapes)
    #         bin_upscaled = cv2.resize(page_bin.astype(np.uint8, copy=False),
    #                                   tuple(original_shape[::-1]), interpolation=cv2.INTER_NEAREST)

    #         # Find quadrilateral enclosing the page
    #         pred_page_coords = boxes_detection.find_boxes(bin_upscaled.astype(np.uint8, copy=False),
    #                                                       mode='min_rectangle', n_max_boxes=1)

    #         # Draw page box on original image and export it. Add also box coordinates to the txt file
    #         original_img = imread(filename, pilmode='RGB')
    #         if pred_page_coords is not None:
    #             cv2.polylines(original_img, [pred_page_coords[:, None, :]], True, (0, 0, 255), thickness=5)
    #             # Write corners points into a .txt file
    #             txt_coordinates += '{},{}\n'.format(filename, format_quad_to_string(pred_page_coords))
    #         else:
    #             print('No box found in {}'.format(filename))
    #         basename = os.path.basename(filename).split('.')[0]
    #         imsave(os.path.join(output_dir, '{}_boxes.jpg'.format(basename)), original_img)

    #         # Create page region and XML file
    #         page_border = PAGE.Border(coords=PAGE.Point.cv2_to_point_list(pred_page_coords[:, None, :]))
    #         page_xml = PAGE.Page(image_filename=filename, image_width=original_shape[1], image_height=original_shape[0],
    #                              page_border=page_border)
    #         xml_filename = os.path.join(output_pagexml_dir, '{}.xml'.format(basename))
    #         page_xml.write_to_file(xml_filename, creator_name='PageExtractor')

    # # Save txt file
    # with open(os.path.join(output_dir, 'pages.txt'), 'w') as f:
    #     f.write(txt_coordinates)
