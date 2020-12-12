# ^=_ coding: utf-8 _=^
from urllib import parse

import requests

from pytfl.utils.config import PyTYfLConfig
from pytfl.utils import logging


logger = logging.getLogger(__name__)


class TflApiDao:
    tfl_api_url = "https://api.tfl.gov.uk"
    tube_line_mode = "tube"

    def __init__(self):
        self.config = PyTYfLConfig()

    def get_response_from_endpoint(self, endpoint, payload):
        payload = self._create_payload(payload)
        full_url = self.get_full_endpoint_url(endpoint)
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
        final_payload = {"app_id": self.config.app_id, "app_key": self.config.app_key}
        final_payload.update(payload)
        logger.info("Created payload dict: %s", final_payload)
        return final_payload

    @staticmethod
    def get_response_contents(response):
        if 200 <= response.status_code < 300:
            logger.info("Got response %s from URL: %s", response.status_code, response.url)
            return response.json()
        else:
            try:
                response.raise_for_status()
            except requests.exceptions.RequestException:
                logger.exception(
                    "Non-success response: %s from URL: %s", response.status_code, response.url
                )
            else:
                logger.warning(
                    "Odd response from server", status=response.status_code, url=response.url
                )
            return None

    def query_endpoint(self, endpoint, payload=None):
        if payload is None:
            payload = {}
        response = self.get_response_from_endpoint(endpoint, payload)
        contents = self.get_response_contents(response)
        return contents

    def get_single_line_stations(self, line_id):
        single_line_station_endpoint = self.get_single_line_stations_endpoint(line_id)
        all_stations_on_line = self.query_endpoint(single_line_station_endpoint)
        return all_stations_on_line

    def get_all_tube_lines(self):
        logger.info("Getting all tube lines from TfL.")
        tube_lines_endpoint = self.get_tube_lines_endpoint()
        all_tube_lines = self.query_endpoint(tube_lines_endpoint)
        return all_tube_lines

    def get_all_tube_stop_points(self):
        all_tube_stop_point_endpoints = self.get_tube_stop_point_endpoint()
        all_tube_stop_points = self.query_endpoint(all_tube_stop_point_endpoints)
        return all_tube_stop_points

    def get_all_route_station_sequences(self, line_id, service_type="Regular"):
        line_all_route_sequences_endpoint = self.get_line_route_sequence_endpoint(line_id)
        payload = {"serviceTypes": service_type}
        line_all_route_station_sequences = self.query_endpoint(
            line_all_route_sequences_endpoint, payload
        )
        return line_all_route_station_sequences

    # `detail=True` returns some poor quality data (e.g. station lat/long is always 0.0) - avoid for now.
    def get_line_status(self, line_id, detail=False):
        endpoint = self.get_line_status_endpoint(line_id)
        payload = {"detail": detail}
        return self.query_endpoint(endpoint, payload)

    def get_full_endpoint_url(self, endpoint):
        return parse.urljoin(self.tfl_api_url, endpoint)

    def get_tube_lines_endpoint(self):
        return "/".join(["Line", "Mode", self.tube_line_mode])

    def get_tube_stop_point_endpoint(self):
        return "/".join(["StopPoint", "Mode", self.tube_line_mode])

    def get_single_line_stations_endpoint(self, line_id):
        return "/".join(["Line", line_id, "StopPoints"])

    def get_line_route_sequence_endpoint(self, line_id, direction="all"):
        return "/".join(["Line", line_id, "Route", "Sequence", direction])

    def get_line_status_endpoint(self, line_id):
        return "/".join(["Line", line_id, "Status"])
