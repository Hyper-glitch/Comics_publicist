import urllib.parse as urllib
from pathlib import Path

import requests


def main():
    comics_path = 'Files/'
    comics_number = '353'

    Path(comics_path).mkdir(parents=True, exist_ok=True)
    comics_url = get_comics_url(comics_number=comics_number)
    save_comics_content(url=comics_url, path=comics_path)


def save_comics_content(url, path):
    image_content = requests.get(url=url)
    image_name = urllib.urlparse(url).path.split('/')[-1]
    save_path = Path(path, image_name)
    with open(save_path, 'wb') as image:
        image.write(image_content.content)


def get_comics_url(comics_number):
    base_url = 'https://xkcd.com/'
    metadata = '/info.0.json'
    url = f'{base_url}{comics_number}{metadata}'
    response = requests.get(url=url)
    response.raise_for_status()
    return response.json()['img']


if __name__ == '__main__':
    main()
