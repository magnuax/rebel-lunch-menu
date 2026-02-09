import sys
import requests
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image
from urllib.parse import urljoin

PAGE_URL = "https://www.thefoodhub.no/kantine"
SESSION = requests.Session()
EXAMPLE_WIDTH = 6240
EXAMPLE_HEIGHT = 3510

def fetch_image():
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
    image = Image.open(BytesIO(response.content))
    image = image.resize((EXAMPLE_WIDTH, EXAMPLE_HEIGHT))

    return image
