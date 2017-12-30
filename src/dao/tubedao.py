# ^=_ coding: utf-8 _=^
from collections import defaultdict
from dao.tfl_api_dao import TflApiDao
from tube.tubeline import TubeLine
from tube.tubestation import TubeStation


class TubeDao(object):

    def __init__(self):
        self.tfl_api_dao = TflApiDao()

    def get_all_tube_lines(self):
        tube_lines_raw = self.tfl_api_dao.get_all_tube_lines()
        tube_lines_objects = [TubeLine(tube_line_dict) for tube_line_dict in tube_lines_raw]
        for tube_line in tube_lines_objects:
            stations = self.get_tube_line_stations(tube_line.id)
            tube_line.tube_stations = tuple(stations)
        return tuple(tube_lines_objects)

    def get_tube_line_stations(self, line_id):
        stations_raw = self.tfl_api_dao.get_single_line_stations(line_id)
        stations = map(TubeStation, stations_raw)
        return stations

    def get_tube_stations(self):
        stop_points_raw = self.get_all_tube_stop_points()
        stop_points_by_stop_type = self._arrange_stop_points_by_stop_type(stop_points_raw)
        tube_stations = self._convert_stop_points_dicts_to_tube_stations(stop_points_by_stop_type)
        return tube_stations

    def _convert_stop_points_dicts_to_tube_stations(self, stop_points_by_stop_type_dict):
        tube_stations_dicts = stop_points_by_stop_type_dict['NaptanMetroStation']
        tube_stations = self._create_tube_stations_from_stop_points(tube_stations_dicts)
        return tube_stations

    def get_all_tube_stop_points(self):
        tube_stop_points_response = self.tfl_api_dao.get_all_tube_stop_points()
        tube_stop_points_list = tube_stop_points_response['stopPoints']
        return tube_stop_points_list

    @staticmethod
    def _arrange_stop_points_by_stop_type(tube_stop_points_list):
        stop_type_to_stop_point = defaultdict(list)
        for stop_point in tube_stop_points_list:
            stop_type = stop_point['stopType']
            stop_type_to_stop_point[stop_type].append(stop_point)
        return dict(stop_type_to_stop_point)

    @staticmethod
    def _create_tube_stations_from_stop_points(tube_stations_dict_list):
        tube_stations = map(TubeStation, tube_stations_dict_list)
        return tuple(tube_stations)

