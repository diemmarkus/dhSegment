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
