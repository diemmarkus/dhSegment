# Avis Article Segmentation
The Avis article segmentation tries to automatically detect articles in the Avis.-Blatt collection

- created: 16.10.2018

## Usage
- run
```cmd
python avis.py with D:\avis\configs\config-regions.json
```
- where `config-regions.json` should look something like

```json
{
  "dbPath" : "D:/avis/configs/articles.csv",
  "outDir": "D:/avis/imgs",
  "download": true
}
```

