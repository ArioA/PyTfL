# ^=_ coding: utf-8 _=^
import os
import os.path
import configparser

from pytfl.utils import logging


logger = logging.getLogger(__name__)


def get_config_file_location():
    env_filename = os.environ.get("PYTFL_CONFIG")
    if env_filename:
        config_file_path = os.path.abspath(env_filename)
    else:
        current_dir = os.path.abspath(".")
        config_file_path = os.path.join(current_dir, "PyTfl.conf")
    return config_file_path


class PyTYfLConfig:

    config_file_location = get_config_file_location()
    config_parser_dict = None

    def __init__(self):
        config_dict = self.initialise_config_parser_dict()

        self.app_id = config_dict["apiCredentials"]["app_id"]
        self.app_key = config_dict["apiCredentials"]["app_key"]

    @classmethod
    def initialise_config_parser_dict(cls):
        if cls.config_parser_dict is None:
            config_parser = configparser.ConfigParser()

            config_parser.read(cls.config_file_location, "utf-8")
            cls.config_parser_dict = config_parser
            logger.info("Initialised config from file: %s", cls.config_file_location)

        return cls.config_parser_dict
