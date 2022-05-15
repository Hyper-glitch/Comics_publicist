import urllib.parse as urllib

import requests

from exceptions import VkUserAuthFailed


class VkApi:
    def __init__(self, access_token, api_version):
        self.base_url = 'https://api.vk.com/method/'
        self.base_params = {
            'access_token': access_token,
            'v': api_version,
        }
        self.session = requests.Session()

    def get_group_id(self, group_name):
        endpoint = 'groups.get'
        url = urllib.urljoin(self.base_url, endpoint)
        params = dict(self.base_params.items() | {'extended': 1}.items())
        response = self.session.get(url=url, params=params)

        if response.json().get('error'):
            message = 'User authorization failed: no access_token passed.'
            raise VkUserAuthFailed(message=message)

        groups = response.json().get('response')['items']
        for group in groups:
            if group_name in group['name']:
                return group['id']

    def get_upload_img_url(self, group_id):
        endpoint = 'photos.getWallUploadServer'
        url = urllib.urljoin(self.base_url, endpoint)
        params = dict(self.base_params.items() | {'group_id': group_id}.items())
        response = self.session.get(url=url, params=params)

        if response.json().get('error'):
            message = 'User authorization failed: no access_token passed.'
            raise VkUserAuthFailed(message=message)

        return response.json()['response'].get('upload_url')
