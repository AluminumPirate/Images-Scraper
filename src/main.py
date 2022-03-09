import os
import random
import string
from random import randint
from time import perf_counter

import requests
from bs4 import BeautifulSoup


def get_random_string(size=7):
    return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=size))


def imagedown(download_url, folder):
    try:
        os.mkdir(os.path.join(os.getcwd(), folder))
        print(f'Created folder {folder}')
        os.chdir(os.path.join(os.getcwd(), folder))
    except Exception as ex:
        print(f'Error creating folder\n{ex}')
        return

    downloaded = 0
    try:
        r = requests.get(download_url, headers={"Accept-Language": "en-US,en;q=0.9",
                                                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"})
        soup = BeautifulSoup(r.text, 'html.parser')
        temp_images = soup.find_all('img')

        if temp_images and 'www.macys.com' in temp_images[0]:
            images = []
            for image in temp_images:
                if 'data-name' in image.attrs and image.attrs['data-name'] == 'img':
                    images.append(image)
        else:
            images = temp_images

        for idx, image in enumerate(images):
            if 'src' in image.attrs:
                link = image['src']
                if 'http' in link:
                    filename = folder + '_' + str(downloaded) + '_fl.jpg'
                    with open(filename, 'wb') as f:
                        im = requests.get(link)
                        f.write(im.content)
                        print(f'Written {idx}: {filename}')
                        downloaded += 1
            else:
                idx -= 1
    except Exception as ex:
        print(f'Unexpected error\n{ex}')

    os.chdir(os.path.join(os.getcwd(), '..'))
    return downloaded


def scrape(urls):
    MIN = 6
    MAX = 12

    total_start_time = perf_counter()
    total_downloads = 0

    os.chdir(os.path.join(os.getcwd(), 'images'))

    for url in urls:
        print(f'Start scraping page: {url}')
        start_time = perf_counter()
        downloads_counter = imagedown(url, get_random_string(randint(MIN, MAX)) + '_fl')
        total_downloads += downloads_counter
        end_time = perf_counter()

        print(f'Script downloaded {downloads_counter} images in {end_time - start_time} seconds')
    total_end_time = perf_counter()

    print(f'Total Downloads: {total_downloads} in {total_end_time - total_start_time} seconds')


def get_urls():
    urls = []
    with open("tabs_output.txt", "r", encoding="utf8") as f:
        lines = f.readlines()

    with open("urls.txt", "w") as f:
        for line in lines:
            if "http" in line:
                urls.append(line.replace('\n', ''))
                f.write(line)
    print('Got list of urls')
    return urls


if __name__ == "__main__":
    urls = get_urls()
    scrape(urls)
