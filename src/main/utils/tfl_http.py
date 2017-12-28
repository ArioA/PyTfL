# ^=_ coding: utf-8 _=^

from main.utils.config import PyTYfLConfig
import requests


class TflHttp(object):

    def __init__(self):
        self.config = PyTYfLConfig()

    def get_response_from_endpoint(self, endpoint):
        payload = {'app_id': self.config.app_id, 'app_key': self.config.app_key}
        full_url = self.config.get_full_endpoint_url(endpoint)
        response = requests.get(full_url, params=payload)
        return response

    @staticmethod
    def get_response_contents(response):
        if 200 <= response.status_code < 300:
            return response.json()

    def get_contents_from_endpoint(self, endpoint):
        response = self.get_response_from_endpoint(endpoint)
        contents = self.get_response_contents(response)
        return contents

    def get_all_tube_lines(self):
        tube_lines_endpoint = self.config.get_tube_lines_endpoint()
        all_tube_lines = self.get_contents_from_endpoint(tube_lines_endpoint)
        return all_tube_lines
