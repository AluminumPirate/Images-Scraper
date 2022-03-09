import random
import string

from src.config import *


def get_random_string(size=7):
    return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=size))


def get_urls():
    urls = []

    with open(TABS_OUTPUT_FILE, "r", encoding="utf8") as f:
        lines = f.readlines()

    with open(URLS_FILE_PATH, "w") as f:
        for line in lines:
            if "http" in line:
                urls.append(line.replace('\n', ''))
                f.write(line)
    print('Got list of urls')
    return urls
