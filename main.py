import urllib.parse as urllib
from pathlib import Path

import requests


def main():
    comics_path = 'Files/'
    comics_number = '353'

    Path(comics_path).mkdir(parents=True, exist_ok=True)
    comics_img = get_comics_img(comics_number=comics_number)
    save_comics_content(url=comics_img, path=comics_path)


def save_comics_content(url, path):
    comics = requests.get(url=url)
    comics_name = urllib.urlparse(url).path.split('/')[-1]
    save_path = Path(path, comics_name)
    with open(save_path, 'wb') as image:
        image.write(comics.content)


def get_comics_img(comics_number):
    base_url = 'https://xkcd.com/'
    metadata = '/info.0.json'
    url = f'{base_url}{comics_number}{metadata}'
    response = requests.get(url=url)
    response.raise_for_status()
    comment = response.json()['alt']
    image = response.json()['img']
    return image


if __name__ == '__main__':
    main()
