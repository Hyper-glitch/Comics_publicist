import os
import random
import time
from pathlib import Path

from dotenv import load_dotenv

from apis import VkApi, ComicsApi


def publish_comics_vk_public():
    """The main logic for running the whole program."""
    load_dotenv()

    vk_access_token = os.environ.get("VK_ACCESS_TOKEN")
    vk_api_version = 5.131
    vk_group_name = 'XKCD'

    comics_path = 'Files/'
    Path(comics_path).mkdir(parents=True, exist_ok=True)

    comics_api = ComicsApi()
    last_comic = comics_api.get_comic()
    random_comic_number = random.randint(1, last_comic['num'])
    random_comic = comics_api.get_comic(comic_number=random_comic_number)
    comics_api.save_comics_content(url=random_comic['img'], path=comics_path)

    vk_instance = VkApi(access_token=vk_access_token, api_version=vk_api_version)
    group_id = vk_instance.get_group_id(group_name=vk_group_name)
    upload_img_url = vk_instance.get_upload_img_url(group_id=group_id)
    upload_img_info = vk_instance.upload_img_to_server(upload_url=upload_img_url)
    saved_img_info = vk_instance.save_img_to_public(upload_img_info=upload_img_info)
    post_id = vk_instance.post_img(
        message=last_comic['alt'], media_id=saved_img_info['id'],
        owner_id=saved_img_info['owner_id'], group_id=group_id,
    )


if __name__ == '__main__':
    while True:
        publish_comics_vk_public()
        time.sleep(5)
