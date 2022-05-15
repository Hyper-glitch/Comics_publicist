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

    def get_groups(self):

        endpoint = 'groups.get'
        url = urllib.urljoin(self.base_url, endpoint)
        response = self.session.get(url=url, params=self.base_params)
        response.raise_for_status()
        return response.json()
