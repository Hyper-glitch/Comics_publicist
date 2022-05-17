"""Module with VK and comics site APIs."""
import urllib.parse as urllib
from pathlib import Path

import requests

from exceptions import (VkUserAuthFailed, UploadPhotoError, SavePhotoError, PostWallImgError)


class VkApi:
    """Class to interact with VK API."""
    def __init__(self, access_token, api_version):
        self.base_url = 'https://api.vk.com/method/'
        self.base_params = {
            'access_token': access_token,
            'v': api_version,
        }
        self.session = requests.Session()

    def get_json(self, url: str, params: dict) -> dict:
        """Get content in json format, raise if error response.
        :param url: - url for make a get request.
        :param params: - needed parameters for make a success request.
        :returns: comic_info - all received information about comic.
        """
        response = self.session.get(url=url, params=params)
        jsonify_response = response.json()
        error = jsonify_response.get('error')
        self.check_on_error(error, exception=VkUserAuthFailed)
        return jsonify_response['response']

    def get_group_id(self, group_name: str) -> int:
        """Get content in json format, raise if error response.
        :param group_name: - group name for getting its id.
        :returns: group_id - group id.
        """
        endpoint = 'groups.get'
        url = urllib.urljoin(self.base_url, endpoint)
        params = {'extended': 1}
        params.update(self.base_params)
        groups = self.get_json(url=url, params=params).get('items')

        for group in groups:
            if group_name in group['name']:
                return group['id']

    def get_upload_img_url(self, group_id: int) -> str:
        """Get url for upload an image to the server.
        :param group_id: - group name for getting its id.
        :returns: upload_img_url - url for upload an image.
        """
        endpoint = 'photos.getWallUploadServer'
        url = urllib.urljoin(self.base_url, endpoint)
        params = {'group_id': group_id}
        params.update(self.base_params)
        upload_img_url = self.get_json(url=url, params=self.base_params).get('upload_url')
        return upload_img_url

    def upload_img_to_server(self, img_path: str, upload_url: str) -> dict:
        """Make post request for uploading an image to the server.
        :param img_path: - path to an image.
        :param upload_url: - url for upload an image.
        :returns: upload_img_info - needed information for save the image to vk public.
        """
        with open(f'{img_path}', 'rb') as image:
            params = {'photo': image}
            response = self.session.post(url=upload_url, files=params)
        upload_img_info = response.json()

        error = response.json().get('error')
        self.check_on_error(error, exception=UploadPhotoError)
        return upload_img_info

    def save_img_to_public(self, upload_img_info: dict) -> dict:
        """Make post request for saving an image to the public vk.
        :param upload_img_info: - needed information for save the image to vk public.
        :returns: saved_img_info - all information of saved image.
        """
        endpoint = 'photos.saveWallPhoto'
        url = urllib.urljoin(self.base_url, endpoint)
        upload_img_info.update(self.base_params)
        response = self.session.post(url=url, params=upload_img_info)

        error = response.json().get('error')
        self.check_on_error(error, exception=SavePhotoError)
        saved_img_info = response.json()['response'][0]
        return saved_img_info

    def post_img(self, message, media_id, owner_id, group_id):
        """Make post request for saving an image to the public vk.
        :param message: - The text of the message (required if the attachments parameter is not set).
        :param media_id: - Media application identifier.
        :param owner_id: - ID of the owner of the media application.
        :param group_id: - The ID of the user or community on whose wall the post is to be posted.
        :returns: post_id - Upon successful completion, returns the ID of the created record.
        """
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
    def check_on_error(error: dict, exception):
        """Check and raise an exception if response has errors.
        :param error: - Error parameter from response.
        :param exception: - Exception depending on error.
        """
        if error:
            message = error['error_msg']
            raise exception(message)
        return


class ComicsApi:
    """Class to interact with xkcd comics API."""
    def __init__(self):
        self.base_url = 'https://xkcd.com/'
        self.data_format = '/info.0.json'

    def get_comic(self, comic_number: int = None) -> dict:
        """Get comic information in json format.
        :param comic_number: - comic index number.
        :returns: comic_info - all received information about comic.
        """
        if comic_number:
            url = f'{self.base_url}{comic_number}{self.data_format}'
        else:
            url = urllib.urljoin(self.base_url, self.data_format)
        response = requests.get(url=url)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def save_comics_content(url: str, path: Path):
        """Save comic image in folder.
        :param url: - url for getting image.
        :param path: - save image path.
        """
        comics = requests.get(url=url)
        with open(path, 'wb') as image:
            image.write(comics.content)
