#!/usr/bin/env python

from sacred import Experiment

# our inlcudes
from dh_segment.avis.databaseLoader import download_images_using_csv


ex = Experiment('avis')

@ex.config
def default_config():
    dbPath    = None          # csv database path
    outDir    = None          # output directory
    download  = True          # download new images

@ex.automain
def run(dbPath, outDir, _config):

    if _config.get('download'):
        download_images_using_csv(dbPath, outDir)

    print('zum abschied sag ich leise ...')