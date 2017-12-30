# ^=_ coding: utf-8 _=^

from collections import defaultdict
from tube.tubeline import TubeLine
from tube.tubestation import TubeStation
from utils import logging
from utils.tfl_http import TflHttp

logger = logging.getLogger(__name__)


class TubeNetwork(object):

    def __init__(self):
        self.api_communicator = TflHttp()
        self.tube_lines = self.create_tube_lines()

    def create_tube_lines(self):
        tube_lines_raw = self.api_communicator.get_all_tube_lines()
        tube_lines_objects = map(TubeLine, tube_lines_raw)
        return tuple(tube_lines_objects)

    def get_tube_stop_points(self):
        tube_stop_points_response = self.api_communicator.get_all_tube_stop_points()
        tube_stop_points_list = tube_stop_points_response['stopPoints']
        return tube_stop_points_list

    def arrange_stop_points_by_stop_type(self, tube_stop_points_list):
        stop_type_to_stop_point = defaultdict(list)
        for stop_point in tube_stop_points_list:
            stop_type = stop_point['stopType']
            stop_type_to_stop_point[stop_type].append(stop_point)
        return dict(stop_type_to_stop_point)

    def create_tube_stations_from_stop_points(self, tube_stations_dict_list):
        tube_stations = map(TubeStation, tube_stations_dict_list)
        return tuple(tube_stations)

    def convert_stop_points_dicts_to_tube_stations(self, stop_points_by_stop_type_dict):
        tube_stations_dicts = stop_points_by_stop_type_dict['NaptanMetroStation']
        tube_stations = self.create_tube_stations_from_stop_points(tube_stations_dicts)
        return tube_stations

    def get_tube_stations(self):
        stop_points_raw = self.get_tube_stop_points()
        stop_points_by_stop_type = self.arrange_stop_points_by_stop_type(stop_points_raw)
        tube_stations = self.convert_stop_points_dicts_to_tube_stations(stop_points_by_stop_type)
        return tube_stations
