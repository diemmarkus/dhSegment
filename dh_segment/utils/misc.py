#!/usr/bin/env python
__license__ = "GPL"

import tensorflow as tf
import json
import pickle
from hashlib import sha1
from random import shuffle


def parse_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)


def dump_json(filename, dict):
    with open(filename, 'w') as f:
        json.dump(dict, f, indent=4, sort_keys=True)


def load_pickle(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)


def dump_pickle(filename, obj):
    with open(filename, 'wb') as f:
        return pickle.dump(obj, f)


def hash_dict(params):
    return sha1(json.dumps(params, sort_keys=True).encode()).hexdigest()

def shuffled(l: list) -> list:
    ll = l.copy()
    shuffle(ll)
    return ll

def download_image(url: str, outDir: str = '', filename: str = '', overwrite: bool = False) -> bool:
    import requests
    import os

    os.makedirs(outDir, exist_ok=True)

    # try parsing the filename
    if not filename:
        us = url.split('/')
        nIdx = us.index('image')+1

        # create filename with extension
        filename = us[nIdx] + '.' + us[-1].split('.')[1]

    filePath = os.path.join(outDir, filename)

    if not overwrite and os.path.exists(filePath):
        return

    with open(filePath, 'wb') as handle:

        response = requests.get(url, stream=True)

        if not response.ok:
            print(response)
            return False

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)

        return True

    return False
