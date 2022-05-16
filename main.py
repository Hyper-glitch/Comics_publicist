import os
import urllib.parse as urllib
from pathlib import Path

import requests
from dotenv import load_dotenv

from vk_api import VkApi


def publish_comics_to_vk():
    """The main logic for running the whole program."""
    load_dotenv()

    vk_access_token = os.environ.get("VK_ACCESS_TOKEN")
    vk_api_version = 5.131
    vk_group_name = 'XKCD'

    comics_path = 'Files/'
    comics_number = '353'

    Path(comics_path).mkdir(parents=True, exist_ok=True)
    comics_img = get_comics_img(comics_number=comics_number)
    save_comics_content(url=comics_img, path=comics_path)

    vk_instance = VkApi(access_token=vk_access_token, api_version=vk_api_version)
    group_id = vk_instance.get_group_id(group_name=vk_group_name)
    upload_img_url = vk_instance.get_upload_img_url(group_id=group_id)
    upload_img_info = vk_instance.upload_img_to_server(upload_url=upload_img_url)
    saved_img = vk_instance.save_img_to_public(upload_img_info=upload_img_info)


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
    publish_comics_to_vk()
