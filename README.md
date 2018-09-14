# dhSegment

dhSegment allows you to extract content (segment regions) from different type of documents. See [some examples here](https://dhlab-epfl.github.io/dhSegment/).

The corresponding paper is now available on [arxiv](https://arxiv.org/abs/1804.10371).

It was created by [Benoit Seguin](https://twitter.com/Seguin_Be) and Sofia Ares Oliveira at DHLAB, EPFL.

## Installation and requirements
 See `INSTALL.md` to install environment and to use `dh_segment` package.
 
 *NB : a good nvidia GPU (6GB RAM at least) is most likely necessary to train your own models. We assume CUDA and cuDNN are installed.*

## Usage
#### Training
* You need to have your training data in a folder containing `images` folder and `labels` folder. The pairs (images, labels) need to have the same name (it is not mandatory to have the same extension file, however we recommend having the label images as `.png` files). 
* The annotated images in `label` folder are (usually) RGB images with the regions to segment annotated with a specific color
* The file containing the classes has the format show below, where each row corresponds to one class (including 'negative' or 'background' class) and each row has 3 values for the 3 RGB values. Of course each class needs to have a different code.
``` class.txt
0 0 0
0 255 0
...
```
* [`sacred`](https://sacred.readthedocs.io/en/latest/quickstart.html) package is used to deal with experiments and trainings. Have a look at the documentation to use it properly.

In order to train a model, you should run `python train.py with <config.json>`

## Demo
This demo shows the usage of dhSegment for page document extraction. It trains a model from scratch (optional) using the [READ-BAD dataset](https://arxiv.org/abs/1705.03311) and the annotations of [pagenet](https://github.com/ctensmeyer/pagenet/tree/master/annotations) (annotator1 is used).
In order to limit memory usage, the images in the dataset we provide have been downsized to have 1M pixels each.

__How to__


1. Get the annotated dataset [here](https://github.com/dhlab-epfl/dhSegment/releases/download/v0.2/pages.zip), which already contains the folders `images` and `labels` for training, validation and testing set. Unzip it into `model/pages`. 
```
cd demo/
wget https://github.com/dhlab-epfl/dhSegment/releases/download/v0.2/pages.zip
unzip pages.zip
cd ..
```
2. (Only needed if training from scratch) Download the pretrained weights for ResNet :
```
cd pretrained_models/
python download_resnet_pretrained_model.py
cd ..
```
3. You can train the model from scratch with: 
    `python train.py with demo/demo_config.json` but because this takes quite some time,
    we recommend you to skip this and just download the [provided model](https://github.com/dhlab-epfl/dhSegment/releases/download/v0.2/model.zip) (download and unzip it in `demo/model`)
```
cd demo/
wget https://github.com/dhlab-epfl/dhSegment/releases/download/v0.2/model.zip
unzip model.zip
cd ..
```
4. (Only if training from scratch) You can visualize the progresses in tensorboard by running `tensorboard --logdir .` in the `demo` folder.
5. Run `python demo.py`
6. Have a look at the results in `demo/processed_images`

## Cheat Sheet Markus

```console
 source ~/READ/dh-env/bin/activate
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda-9.0/lib64/
python test.py
```

training page split:
```console
 python train.py with ./data/config/page-split-config.json
```

test page split:
```console
 python test-page-split.py with ./data/config/page-split-test.json
```

## Create Page Split Database

```cmd
cd Benchmarking/lib/database
REM make a flat copy of the labels (20000 == all)
python cdb.py --ext "png" --flatcopy --copyto C:\read\cBAD\page-split\dataset2\labels C:\read\cBAD\page-split\versions\READ-ICDAR2017-cBAD-dataset-v3 20000
REM make a flat copy of the images
python cdb.py --ext "jpg" --flatcopy --copyto C:\read\cBAD\page-split\dataset2\images C:\read\cBAD\page-split\versions\READ-ICDAR2017-cBAD-dataset-v3 20000

REM split the datasets (into train/eval/test)
python split.py --train 0.33 --eval 0.33 C:\read\cBAD\page-split\dataset2\labels C:\read\cBAD\page-split\dataset2\labels-split
python split.py --train 0.33 --eval 0.33 C:\read\cBAD\page-split\dataset2\images C:\read\cBAD\page-split\dataset2\images-split

```