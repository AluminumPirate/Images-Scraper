from src.utils import get_urls
from src.scraper import download_images_to_directory
from src.config import *


def main():
    urls = get_urls()
    total_downloads, total_time = download_images_to_directory(urls)
    with open(LOG_FILE_NAME, 'a') as f:
        f.write(
            f'\n\nSUMMARY:\nTotal downloads from {len(urls)} links: {total_downloads}\nScript ran for: {total_time} seconds\n')
        print(f'\n\nSUMMARY:\nTotal downloads from {len(urls)} links:{total_downloads}\nIt took: {total_time} seconds')


if __name__ == "__main__":
    main()
