from lunchmenu.format import format_menu_entry
from lunchmenu.fetch import fetch_image
import pytesseract

TESS_CONFIG = r"--oem 1 --psm 6" 

# Coordinates of upper left (1) and lower right (2) corners of the rectangles for each day
WEEKDAY_CORNERS = {
    "monday":    ((220,  680),  (2000, 2000)), # 1780 x 1320
    "tuesday":   ((2000, 680),  (4200, 2000)), # 2200 x 1320
    "wednesday": ((4200, 680),  (6000, 2000)), # 1800 x 1320
    "thursday":  ((2000, 2000), (4200, 3200)), # 2200 x 1200
    "friday":    ((4200, 2000), (6000, 3100)), # 1800 x 1000
}

# y coordinate of the line that divides daily entry into non-vegetarian and vegetarian options.
WEEKDAY_ENTRY_SLICE ={
    "monday":    720,
    "tuesday":   680,
    "wednesday": 720,
    "thursday":  700,
    "friday":    700
}

def menu_of_the_day(weekday, image=None):
    
    if image is None:
        image = fetch_image()
        
    if weekday not in WEEKDAY_CORNERS:
        raise ValueError("weekday not found!")
    
    corners = WEEKDAY_CORNERS[weekday]
    corner_1 = (int(corners[0][0]), int(corners[0][1]))
    corner_2 = (int(corners[1][0]), int(corners[1][1]))
    
    slice_idx = int(WEEKDAY_ENTRY_SLICE[weekday.lower()])

    menu_entry = image.crop((*corner_1, *corner_2))
    top_half    = menu_entry.crop((0, 0, menu_entry.width, slice_idx))
    bottom_half = menu_entry.crop((0, slice_idx, menu_entry.width, menu_entry.height))
        
    top_raw_text    = pytesseract.image_to_string(top_half, lang="nor+eng", config=TESS_CONFIG)
    bottom_raw_text = pytesseract.image_to_string(bottom_half, lang="nor+eng", config=TESS_CONFIG)

    combined = format_menu_entry(top_raw_text, includes_title=True) + "\n" + format_menu_entry(bottom_raw_text)

    return combined

def menu_of_the_week(image=None):
    
    if image is None:
        image = fetch_image()
        
    full_menu = ""
    for weekday in WEEKDAY_CORNERS.keys():
        full_menu += menu_of_the_day(weekday, image) + "\n"
    
    return full_menu