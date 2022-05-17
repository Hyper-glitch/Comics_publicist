import os
import random
import time
import urllib.parse as urllib
from pathlib import Path

from dotenv import load_dotenv

from apis import VkApi, ComicsApi


def post_comics_vk_public():
    """The main logic of getting random comic from 'https://xkcd.com/' and post it on the public wall in VK."""
    load_dotenv()

    vk_access_token = os.environ.get("VK_ACCESS_TOKEN")
    publication_frequency = float(os.environ.get("PUBLICATION_FREQUENCY"))
    vk_api_version = 5.131
    vk_group_name = 'XKCD'
    start_random_range = 1
    comics_dir = 'Files/'
    Path(comics_dir).mkdir(parents=True, exist_ok=True)

    comics_api = ComicsApi()
    vk_instance = VkApi(access_token=vk_access_token, api_version=vk_api_version)

    while True:
        last_comic = comics_api.get_comic()
        random_comic_number = random.randint(start_random_range, last_comic['num'])
        random_comic = comics_api.get_comic(comic_number=random_comic_number)
        random_comic_name = urllib.urlparse(random_comic['img']).path.split('/')[-1]
        comic_path = Path(comics_dir, random_comic_name)
        comics_api.save_comics_content(url=random_comic['img'], path=comic_path)

        group_id = vk_instance.get_group_id(group_name=vk_group_name)
        uploaded_img_url = vk_instance.get_upload_img_url(group_id=group_id)
        uploaded_img = vk_instance.upload_img_to_server(img_path=comic_path, upload_url=uploaded_img_url)
        saved_img = vk_instance.save_img_to_public(upload_img_info=uploaded_img)
        vk_instance.post_img(
            message=random_comic['alt'], media_id=saved_img['id'],
            owner_id=saved_img['owner_id'], group_id=group_id,
        )
        if os.path.isfile(comic_path) or os.path.islink(comic_path):
            os.remove(comic_path)
        time.sleep(publication_frequency)


if __name__ == '__main__':
    post_comics_vk_public()
