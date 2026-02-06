import sys
import requests
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image
from urllib.parse import urljoin
import pytesseract
from utils import style
Image.MAX_IMAGE_PIXELS = None

TESS_CONFIG = r"--oem 1 --psm 6" 
PAGE_URL = "https://www.thefoodhub.no/kantine"
SESSION = requests.Session()

# Coordinates of upper left (1) and lower right (2) corners of the rectangles for each day
WEEKDAY_CORNERS = {
    "monday":    ((220,  680),  (2000, 2000)), # 1780 x 1320
    "tuesday":   ((2000, 680),  (4200, 2000)), # 2200 x 1320
    "wednesday": ((4200, 680),  (6000, 2000)), # 1800 x 1320
    "thursday":  ((2000, 2000), (4200, 3200)), # 2200 x 1200
    "friday":    ((4200, 2000), (6000, 3000)), # 1800 x 1000
}

WEEKDAY_ENTRY_SLICE ={
    "monday":    720,
    "tuesday":   680,
    "wednesday": 720,
    "thursday":  700,
    "friday":    600
}

ALLERGENS = {"egg":     True,
            "fish":     True,
            "gluten":   True,
            "melk":     True,
            "nøtter":   True,
            "peanøtter": True,
            "selleri":  True,
            "sennep":   True,
            "sesam":    True,
            "sesamfrø": True,
            "skalldyr": True,
            "soya":     True,
            "sulfitt":  True,
            "bløtdyr":  True,
            "lupin":    True}

request = SESSION.get(PAGE_URL, timeout=10, stream=True)
request.raise_for_status()

parsed = BeautifulSoup(request.text, "html.parser")
result = parsed.find("a", string=lambda button_text: button_text and "Ukens meny" in button_text)

if not result or not result.get("href"):
    print("Link not found", file=sys.stderr)
    sys.exit(1)

menu_url = urljoin(PAGE_URL, result["href"])
response = SESSION.get(menu_url, timeout=10, stream=True)
response.raise_for_status()
img = Image.open(BytesIO(response.content))


def looks_like_allergens(line):
    split = line.split(",")
    
    for part in split:
        part = part.strip().lower()
        if part in ALLERGENS:
            return True                    

    return False

def parse_menu_entry(raw_text, includes_title=False):

    formatted = ""
    i = 0

    split = raw_text.splitlines()
    filtered = [line for line in split if line.strip() != ""]
    is_not_empty = len(filtered) > 0


    if includes_title and is_not_empty:
        title = filtered.pop(0)
        formatted += "\n-------\n"
        formatted += style(title, "bold")
        formatted += "\n-------\n"


    lines = []

    if len(filtered) > 0:
        lines.append(style(filtered[0], "bold") + "\n")    
    if len(filtered) > 1:
        lines.append(style(filtered[1], "normal") + "\n")
    if len(filtered) > 2:
        lines.append(style(filtered[2], "italic") + "\n")

    formatted += "".join(lines)
    
    return formatted



def menu_of_the_day(weekday):
    
    if weekday not in WEEKDAY_CORNERS:
        raise ValueError("weekday not found!")
    
    corner_1, corner_2 = WEEKDAY_CORNERS[weekday]
    slice_idx = WEEKDAY_ENTRY_SLICE[weekday.lower()]

    menu_entry = img.crop((*corner_1 , *corner_2))
    top_half    = menu_entry.crop((0, 0, menu_entry.width, slice_idx))
    bottom_half = menu_entry.crop((0, slice_idx, menu_entry.width, menu_entry.height))
        
    top_raw_text    = pytesseract.image_to_string(top_half, lang="nor+eng", config=TESS_CONFIG)
    bottom_raw_text = pytesseract.image_to_string(bottom_half, lang="nor+eng", config=TESS_CONFIG)

    combined = parse_menu_entry(top_raw_text, includes_title=True) + "\n" + parse_menu_entry(bottom_raw_text)

    return combined


def menu_of_the_week():

    full_menu = ""
    import matplotlib.pyplot as plt

    for weekday in WEEKDAY_CORNERS.keys():
        
        full_menu += menu_of_the_day(weekday) + "\n"
    
    return full_menu

if __name__ == "__main__":
    from utils import arg_parser
    import datetime

    parser = arg_parser()
    
    if parser["full"]:
        print(menu_of_the_week())
        
    elif parser["today"]:
        today = datetime.date.today()
        weekday = today.strftime("%A").lower()
        print(menu_of_the_day(weekday))
    
    elif parser["weekday"]:
        weekday = parser["weekday"].lower()
        print(menu_of_the_day(weekday))
        