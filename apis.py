import urllib.parse as urllib
from pathlib import Path

import requests

from exceptions import (VkUserAuthFailed, UploadPhotoError, SavePhotoError, PostWallImgError)


class VkApi:
    def __init__(self, access_token, api_version):
        self.base_url = 'https://api.vk.com/method/'
        self.base_params = {
            'access_token': access_token,
            'v': api_version,
        }
        self.session = requests.Session()

    def get_json(self, url, params):
        response = self.session.get(url=url, params=params)
        jsonify_response = response.json()
        error = jsonify_response.get('error')
        self.check_on_error(error, exception=VkUserAuthFailed)
        return jsonify_response['response']

    def get_group_id(self, group_name):
        endpoint = 'groups.get'
        url = urllib.urljoin(self.base_url, endpoint)
        params = {'extended': 1}
        params.update(self.base_params)
        groups = self.get_json(url=url, params=params).get('items')

        for group in groups:
            if group_name in group['name']:
                return group['id']

    def get_upload_img_url(self, group_id):
        endpoint = 'photos.getWallUploadServer'
        url = urllib.urljoin(self.base_url, endpoint)
        params = {'group_id': group_id}
        params.update(self.base_params)
        upload_img_url = self.get_json(url=url, params=self.base_params).get('upload_url')
        return upload_img_url

    def upload_img_to_server(self, upload_url):
        with open('Files/python.png', 'rb') as image:
            params = {'photo': image}
            response = self.session.post(url=upload_url, files=params)
        upload_img_info = response.json()

        error = response.json().get('error')
        self.check_on_error(error, exception=UploadPhotoError)
        return upload_img_info

    def save_img_to_public(self, upload_img_info):
        endpoint = 'photos.saveWallPhoto'
        url = urllib.urljoin(self.base_url, endpoint)
        upload_img_info.update(self.base_params)
        response = self.session.post(url=url, params=upload_img_info)

        error = response.json().get('error')
        self.check_on_error(error, exception=SavePhotoError)
        saved_img_info = response.json()['response'][0]
        return saved_img_info

    def post_img(self, message, media_id, owner_id, group_id):
        endpoint = 'wall.post'
        media_type = 'photo'
        url = urllib.urljoin(self.base_url, endpoint)
        attachments = f'{media_type}{owner_id}_{media_id}'
        params = {
            'owner_id': -group_id,
            'from_group': 1,
            'message': message,
            'attachments': attachments,
        }
        params.update(self.base_params)
        response = self.session.post(url=url, params=params)

        error = response.json().get('error')
        self.check_on_error(error, exception=PostWallImgError)
        post_id = response.json()['response']['post_id']
        return post_id

    @staticmethod
    def check_on_error(error, exception):
        if error:
            message = error['error_msg']
            raise exception(message)
        return


class ComicsApi:
    def __init__(self):
        self.base_url = 'https://xkcd.com/'
        self.data_format = '/info.0.json'

    def get_comic(self, comic_number=None):
        if comic_number:
            url = f'{self.base_url}{comic_number}{self.data_format}'
        else:
            url = urllib.urljoin(self.base_url, self.data_format)
        response = requests.get(url=url)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def save_comics_content(url, path):
        comics = requests.get(url=url)
        comics_name = urllib.urlparse(url).path.split('/')[-1]
        save_path = Path(path, comics_name)
        with open(save_path, 'wb') as image:
            image.write(comics.content)
