# Avis Article Segmentation
The Avis article segmentation tries to automatically detect articles in the Avis.-Blatt collection

- created: 16.10.2018

## Convert Avis CSV to PAGE
- run
```cmd
python avis.py with D:\avis\configs\config-regions.json
```
- where `config-regions.json` should look something like

```json
{
  "dbPath" : "D:/avis/configs/articles.csv",
  "outDir": "D:/avis/imgs",
  "download": true,
  "createPageXml": true
}
```

## Create Database

- ReadFramework > Page XML > Label Image from XML
- batch process all images with profile `Avis Article`
- config file:

```json
{
  "Labels": [
  {
    "Class" : {
      "id": 4,
      "z-index": 2,
      "name": "separator",
      "alias": ["SeparatorRegion"],
      "color": "#f49b42"
    }
  },
  {
    "Class": {
      "id": 3,
      "name": "article",
      "z-index": 1,
      "alias": [
        "TextRegion"
      ],
      "color": "#8fd3b2"
    }
  }
  ]
}
```

## split database
- clone https://github.com/TUWien/Benchmarking
- split the database using:
```cmd
python split.py --train 0.33 --eval 0.33 E:\avis\18-11-imgs E:\avis\database
python split.py --train 0.33 --eval 0.33 E:\avis\18-11-labels E:\avis\database
```
- move all source `*.jpg` images into `images` (e.g. eval/images)
- move all label `*.png` images into `labels` (e.g. eval/labels)

## train
```bash
source ~/READ/dh-env/bin/activate
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda-9.0/lib64/
python train.py with data/config/avis-train.json
```
where avis-train.json looks like this:
```json
{
  "training_params" : {
      "learning_rate": 5e-5,
      "batch_size": 1,
      "make_patches": false,
      "training_margin" : 0,
      "n_epochs": 30,
      "data_augmentation" : true,
      "data_augmentation_max_rotation" : 0.2,
      "data_augmentation_max_scaling" : 0.2,
      "data_augmentation_flip_lr": true,
      "data_augmentation_flip_ud": true,
      "data_augmentation_color": false,
      "evaluate_every_epoch" : 10
  },
  "pretrained_model_name" : "resnet50",
  "prediction_type": "CLASSIFICATION",
  "train_data" : "data/imgs/train/",
  "eval_data" : "data/imgs/eval/",
  "classes_file" : "data/config/classes.txt",
  "model_output_dir" : "data/avis-cvl-model",
  "gpu" : "1",
  "restore_model" : true
}
```