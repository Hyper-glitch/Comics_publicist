import urllib.parse as urllib

import requests

from exceptions import VkUserAuthFailed, UploadPhotoError, SavePhotoError


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

        if jsonify_response.get('error'):
            message = 'User authorization failed: no access_token passed.'
            raise VkUserAuthFailed(message=message)

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
        if not upload_img_info['photo']:
            raise UploadPhotoError('The photo did not upload to the server')

        return upload_img_info

    def save_img_to_public(self, upload_img_info):
        endpoint = 'photos.saveWallPhoto'
        url = urllib.urljoin(self.base_url, endpoint)
        upload_img_info.update(self.base_params)
        response = self.session.post(url=url, params=upload_img_info)
        error = response.json().get('error')
        if error:
            message = error['error_msg']
            raise SavePhotoError(f'The photo did not save on the server, {message}')

        saved_img = response.json()['response'][0]
        return saved_img
