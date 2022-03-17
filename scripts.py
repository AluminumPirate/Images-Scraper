import os
import ast
from pathlib import Path
from datetime import date
from tkinter import Tk, filedialog

today = date.today().strftime("%d-%m-%Y")

FILENAME = 'take_names.txt'
CHAR_TO_REPLACE = ['(', ')', '{', '}', '\n', '\t']


def get_skus_from_file(filename):
    skus = []
    with open(rf'{filename}', 'r') as f:
        lines = f.readlines()

        for line in lines:
            for char in CHAR_TO_REPLACE:
                line = line.replace(char, '')

            if '/' in line or line == '':
                continue
            skus.append(line)

    return skus


def create_directories_from_sku_list(sku_list, file_path):
    dir_name, basename = os.path.split(file_path)

    root = f"{dir_name}\\"
    try:
        for sku in sku_list:
            create_path = f"{root}\\{sku}"
            # os.mkdirs(create_path)
            Path(create_path).mkdir(parents=True, exist_ok=True)
    except FileExistsError:
        print(f'{basename} already exists')
    except Exception as ex:
        print(f'{ex}')
        return False

    return True


def main():
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)

    file_path = filedialog.askopenfilename()

    skus = get_skus_from_file(file_path)
    success = create_directories_from_sku_list(skus, file_path)

    if success:
        print(f'{len(skus)} folders created for skus:')
        for sku in skus:
            print(sku, end=', ')

        print('Done')


main()