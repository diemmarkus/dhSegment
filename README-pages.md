# Page Split

- created: 10.09.2018
- update: 17.09.2018

This dataset is derived from the cBAD dataset. We manually annotated all page splits and pages by enclosing rectangles.

## Database creation

### Create Database

- ReadFramework > Page XML > Label Image from XML
- batch process all images with profile `Page Split Labels III`
- config file:

```json
{
  "Labels": [
  {
    "Class" : {
      "id": 4,
      "z-index": 2,
      "name": "split",
      "alias": ["SeparatorRegion"],
      "color": "#f49b42"
    }
  },
  {
    "Class": {
      "id": 3,
      "name": "page",
      "z-index": 1,
      "alias": [
        "Border"
      ],
      "color": "#8fd3b2"
    }
  }
  ]
}
```

- split folders (gt only, images only)
- flat copy & add index to filename

```cmd
cd Benchmarking/lib/database
REM make a flat copy of the labels (20000 == all)
python cdb.py --ext "png" --flatcopy --copyto C:\read\cBAD\page-split\dataset3\labels C:\read\cBAD\page-split\versions\READ-ICDAR2017-cBAD-dataset-v3-pages 20000
REM make a flat copy of the images
python cdb.py --ext "jpg" --flatcopy --copyto C:\read\cBAD\page-split\dataset3\images C:\read\cBAD\page-split\versions\READ-ICDAR2017-cBAD-dataset-v3-pages 20000
```

- now we have 2035 images (\*.jpg) with 2035 gt label images (\*.png)
- split the databases into train/eval/test sets

```cmd
REM split the datasets (into train/eval/test)
python split.py --train 0.33 --eval 0.33 C:\read\cBAD\page-split\dataset3\labels C:\read\cBAD\page-split\dataset3\labels-split
python split.py --train 0.33 --eval 0.33 C:\read\cBAD\page-split\dataset3\images C:\read\cBAD\page-split\dataset3\images-split
```

## Train & Test with dhSegment

training page split:

```cmd
 python train.py with ./data/config/page-split-config.json
```

test page split:

```cmd
 python test-page-split.py with ./data/config/page-split-test.json
```
