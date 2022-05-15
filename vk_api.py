import urllib.parse as urllib

import requests


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
        self.base_params.update({'extended': 1})
        response = self.session.get(url=url, params=self.base_params)

        groups = response.json().get('response')['items']
        for group in groups:
            if group_name in group['name']:
                return group['id']

    def get_upload_img_url(self):
        pass
