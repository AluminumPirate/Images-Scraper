from os import path
from datetime import datetime

FAIL_EXT = '_fl'
TABS_OUTPUT_FILE = 'tabs_output.txt'
URLS_DIR = 'urls'
URLS_FILE = 'urls.txt'
LOG_FILE_NAME = datetime.now().strftime("%d-%m-%Y %H-%M-%S") + 'log.txt'
URLS_FILE_PATH = path.join(URLS_DIR, URLS_FILE)
IMAGES_DIR = path.join('images', datetime.now().strftime("%d-%m-%Y %H-%M-%S"))
OPTIONAL_IMAGES_DOWNLOADABLE_ATTRIBUTES = ['src', 'data-src']

HEADERS = {"Accept-Language": "en-US,en;q=0.9",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"}
