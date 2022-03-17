# System imports
import os
from random import randint
from time import perf_counter
import pathlib
import threading

# Scraping Imports
import requests
from bs4 import BeautifulSoup

# Utils imports
from src.utils import get_random_string

from src.config import *


def save_image(folder, downloaded, link):
    filename = folder.replace(FAIL_EXT, '') + '_' + str(downloaded) + '_fl.jpg'
    try:
        with open(filename, 'wb') as f:
            im = requests.get(link)
            f.write(im.content)
    except Exception as ex:
        print(f'{ex}')
        return False

    return True


def get_downloadable_image_links(image):
    links = []
    optional_src = OPTIONAL_IMAGES_DOWNLOADABLE_ATTRIBUTES
    for optional in optional_src:
        if optional in image.attrs:
            links.append(image[optional])

    links = list(set(links))
    return links


def mkdir_and_change_dir(folder):
    try:
        os.mkdir(os.path.join(os.getcwd(), folder))
        print(f'Created folder {folder}')
        os.chdir(os.path.join(os.getcwd(), folder))
    except Exception as ex:
        print(f'Error creating folder\n{ex}')
        return False

    return True


def scrape_url(download_url, folder):
    if not mkdir_and_change_dir(folder):
        return

    downloaded = 0
    try:
        r = requests.get(download_url, headers=HEADERS)
        soup = BeautifulSoup(r.text, 'html.parser')
        images = soup.find_all('img')

        for image in images:
            links = get_downloadable_image_links(image)

            if not links:
                continue

            for link in links:
                if 'http://' in link or 'https://' in link:
                    filename = folder.replace('_fl', '') + '_' + str(downloaded) + '_fl.jpg'
                    if save_image(folder, downloaded, link):
                        print(f'Written {downloaded}: {filename}')
                        downloaded += 1
                else:
                    continue

    except Exception as ex:
        print(f'Unexpected error\n{ex}')

    os.chdir(os.path.join(os.getcwd(), '..'))

    return downloaded


# Enable multithreading
# def download_images_to_directory(urls):
#     for url in urls:
#         threading.Thread(target=download_image_to_directory, args=(url, )).start()


def download_images_to_directory(urls):
    MIN = 6
    MAX = 12

    total_start_time = perf_counter()
    total_downloads = 0

    try:
        pathlib.Path(IMAGES_DIR).mkdir(parents=True, exist_ok=True)
        # if not os.path.exists(IMAGES_DIR):
        #     os.mkdir(IMAGES_DIR)

        os.chdir(os.path.join(os.getcwd(), IMAGES_DIR))
    except Exception as ex:
        print(f'{ex}')
        return

    for url in urls:
        with open(LOG_FILE_NAME, 'a') as f:
            f.write(f'Start scraping page: {url}\n')
        print(f'Start scraping page: {url}')

        start_time = perf_counter()
        downloads_counter = scrape_url(url, get_random_string(randint(MIN, MAX)) + FAIL_EXT)
        total_downloads += downloads_counter
        end_time = perf_counter()

        with open(LOG_FILE_NAME, 'a') as f:
            f.write(f'Script downloaded {downloads_counter} images in {end_time - start_time} seconds\n\n')
        print(f'Script downloaded {downloads_counter} images in {end_time - start_time} seconds')

    total_end_time = perf_counter()

    return total_downloads, (total_end_time - total_start_time)
