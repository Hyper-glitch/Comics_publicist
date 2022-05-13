import urllib.parse as urllib
from pathlib import Path

import requests


def main():
    Path('Files/').mkdir(parents=True, exist_ok=True)
    comics_number = '353'
    comics_url = get_comics_url(comics_number=comics_number)
    comics_content = get_image_content(comics_url=comics_url)
    save_comics(image_content=comics_content)


def get_image_content(comics_url):
    image_content = requests.get(url=comics_url)
    image_name = urllib.urlparse(comics_url).path.split('/')[-1]
    return image_content.content, image_name


def get_comics_url(comics_number):
    base_url = 'https://xkcd.com/'
    metadata = '/info.0.json'
    url = f'{base_url}{comics_number}{metadata}'
    response = requests.get(url=url)
    response.raise_for_status()
    return response.json()['img']


def save_comics(image_content):
    with open('Files/', 'wb') as image:
        image.write(image_content)


if __name__ == '__main__':
    main()
