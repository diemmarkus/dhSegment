#!/usr/bin/env python

from sacred import Experiment

# our inlcudes
from dh_segment.avis.databaseLoader import download_images_using_csv, create_page_xmls


ex = Experiment('avis')


@ex.config
def default_config():
    dbPath = None          # csv database path
    outDir = None          # output directory
    download = True          # download new images
    createPageXml = True          # create GT as PAGE


@ex.automain
def run(dbPath, outDir, _config):

    if _config.get('download'):
        download_images_using_csv(dbPath, outDir)

    if _config.get('createPageXml'):
        create_page_xmls(dbPath, outDir)

    print('zum abschied sag ich leise ...')
