# ^=_ coding: utf-8 _=^

from utils.config import PyTYfLConfig
from utils import logging
import requests


logger = logging.getLogger(__name__)


class TflApiDao(object):
    def __init__(self):
        self.config = PyTYfLConfig()

    def get_response_from_endpoint(self, endpoint, payload):
        payload = self._create_payload(payload)
        full_url = self.config.get_full_endpoint_url(endpoint)
        logger.info("Sending GET request to %s", full_url)
        response = requests.get(full_url, params=payload)
        return response

    def _create_payload(self, payload):
        """
        Creates payload (parameters in HTTP request) to be sent in a request.

        Parameters
        ----------
        payload: dict
            A dictionary with key and values as parameter names and parameter values of
            the HTTP request respectively.

        Returns
        -------
        dict
            Which is the totality of the payload to be sent in the request to TfL's API.
            If the parameter ``payload`` has keys 'app_id' or 'app_key' (or both) then
            these will override the values derived from the PyTfl.conf file.
        """
        credentials_payload = {
            "app_id": self.config.app_id,
            "app_key": self.config.app_key,
        }
        final_payload = credentials_payload.copy()
        final_payload.update(payload)
        logger.info("Created payload dict: %s", final_payload)
        return final_payload

    @staticmethod
    def get_response_contents(response):
        if 200 <= response.status_code < 300:
            logger.info(
                "Got response %s from URL: %s", response.status_code, response.url
            )
            return response.json()
        else:
            logger.info(
                "Non-success response: %s from URL: %s",
                response.status_code,
                response.url,
            )

    def get_contents_from_endpoint(self, endpoint, payload={}):
        response = self.get_response_from_endpoint(endpoint, payload)
        contents = self.get_response_contents(response)
        return contents

    def get_single_line_stations(self, line_id):
        single_line_station_endpoint = self.config.get_single_line_stations_endpoint(
            line_id
        )
        all_stations_on_line = self.get_contents_from_endpoint(
            single_line_station_endpoint
        )
        return all_stations_on_line

    def get_all_tube_lines(self):
        tube_lines_endpoint = self.config.get_tube_lines_endpoint()
        all_tube_lines = self.get_contents_from_endpoint(tube_lines_endpoint)
        return all_tube_lines

    def get_all_tube_stop_points(self):
        all_tube_stop_point_endpoints = self.config.get_tube_stop_point_endpoint()
        all_tube_stop_points = self.get_contents_from_endpoint(
            all_tube_stop_point_endpoints
        )
        return all_tube_stop_points

    def get_all_route_station_sequences(self, line_id, service_type="Regular"):
        line_all_route_sequences_endpoint = self.config.get_line_route_sequence_endpoint(
            line_id
        )
        payload = {"serviceTypes": service_type}
        line_all_route_station_sequences = self.get_contents_from_endpoint(
            line_all_route_sequences_endpoint, payload
        )
        return line_all_route_station_sequences
