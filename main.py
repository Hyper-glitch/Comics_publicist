import os
import random
import urllib.parse as urllib
from pathlib import Path

import requests
from dotenv import load_dotenv

from apis import VkApi


def publish_comics_to_vk():
    """The main logic for running the whole program."""
    load_dotenv()

    vk_access_token = os.environ.get("VK_ACCESS_TOKEN")
    vk_api_version = 5.131
    vk_group_name = 'XKCD'

    comics_path = 'Files/'

    Path(comics_path).mkdir(parents=True, exist_ok=True)
    last_comic = get_last_comic()
    random_comic = random.randint(1, last_comic['num'])

    save_comics_content(url=last_comic['img'], path=comics_path)

    vk_instance = VkApi(access_token=vk_access_token, api_version=vk_api_version)
    group_id = vk_instance.get_group_id(group_name=vk_group_name)
    upload_img_url = vk_instance.get_upload_img_url(group_id=group_id)
    upload_img_info = vk_instance.upload_img_to_server(upload_url=upload_img_url)
    saved_img_info = vk_instance.save_img_to_public(upload_img_info=upload_img_info)
    post_id = vk_instance.post_img(
        message=last_comic['alt'], media_id=saved_img_info['id'],
        owner_id=saved_img_info['owner_id'], group_id=group_id,
    )


def save_comics_content(url, path):
    comics = requests.get(url=url)
    comics_name = urllib.urlparse(url).path.split('/')[-1]
    save_path = Path(path, comics_name)
    with open(save_path, 'wb') as image:
        image.write(comics.content)


def get_last_comic():
    base_url = 'https://xkcd.com/'
    metadata = '/info.0.json'
    url = f'{base_url}{metadata}'
    response = requests.get(url=url)
    response.raise_for_status()
    return response.json()


def get_comic(comic_number):
    base_url = 'https://xkcd.com/'
    metadata = '/info.0.json'
    url = f'{base_url}{comic_number}{metadata}'
    response = requests.get(url=url)
    response.raise_for_status()
    return response.json()


if __name__ == '__main__':
    publish_comics_to_vk()
