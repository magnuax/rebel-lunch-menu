# Rebel Lunch Menu CLI

A slow and comically overengineered tool for accessing the weekly menu at The Food Hub, at Rebel (*Universitetsgata 2, 0164 Oslo*).

The menu is published as an image. This tool:
1. Fetches the menu image from [The Food Hub](https://www.thefoodhub.no/kantine)
2. Crops out relevant weekday sections and menu entries
3. Runs [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) on the cropped out sections
4. Formats and returns dish, sub-header and allergen strings (in norwegian)

### Usage
```
python3 -m lunchmenu.cli [--full] [--today] [--weekday=<day>]
```

### Example
```
$ python3 -m lunchmenu.cli --weekday=wednesday

-------
Onsdag
-------
Uer
Hummer Bisque
Fisk, Skalldyr, Selleri

Daal
Gule Linser & Indisk Popcorn-Blomkal
Egg, Melk, Selleri

```
