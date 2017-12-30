# ^=_ coding: utf-8 _=^

import configparser
from utils import logging
import os.path

logger = logging.getLogger(__name__)


class PyTYfLConfig(object):

    config_file_location = os.path.abspath('../PyTfL.conf')
    config_parser_dict = None

    def __init__(self):
        config_dict = self.initialise_config_parser_dict()

        self.app_id = config_dict['apiCredentials']['app_id']
        self.app_key = config_dict['apiCredentials']['app_key']

        self.tfl_api_url = 'https://api.tfl.gov.uk'

        self.url_format = '{base_url}{endpoint}'

        self.tube_line_mode = 'tube'

        self.line_mode_endpoint = '/Line/Mode/{id}'
        self.tube_stop_point_endpoint = '/StopPoint/Mode/{id}'

    @classmethod
    def initialise_config_parser_dict(cls):
        if cls.config_parser_dict is None:
            config_parser = configparser.ConfigParser()

            config_parser.read(cls.config_file_location, 'utf-8')
            cls.config_parser_dict = config_parser
            logger.info('Initialised config from file: %s', cls.config_file_location)

        return cls.config_parser_dict

    def get_tube_lines_endpoint(self):
        tube_lines_endpoint = self.line_mode_endpoint.format(id=self.tube_line_mode)
        return tube_lines_endpoint

    def get_tube_stop_point_endpoint(self):
        tube_stop_point_endpoint = self.tube_stop_point_endpoint.format(id=self.tube_line_mode)
        return tube_stop_point_endpoint

    def get_full_endpoint_url(self, endpoint):
        return self.url_format.format(base_url=self.tfl_api_url, endpoint=endpoint)
