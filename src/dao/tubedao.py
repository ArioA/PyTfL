# ^=_ coding: utf-8 _=^
from collections import defaultdict
from dao.tfl_api_dao import TflApiDao
from tube.tubeline import TubeLine
from tube.tubestation import TubeStation
from tube.tuberoute import TubeRoute


class TubeDao(object):

    def __init__(self):
        self.tfl_api_dao = TflApiDao()

    def get_all_tube_lines(self):
        tube_lines_raw = self.tfl_api_dao.get_all_tube_lines()
        tube_lines_objects = [TubeLine(tube_line_dict) for tube_line_dict in tube_lines_raw]
        for tube_line in tube_lines_objects:
            stations = self.get_tube_line_stations(tube_line.id)
            tube_line.tube_stations = tuple(stations)
            routes_dict = self.get_line_route_sequences(tube_line.id, 'Regular,Night')
            for service_type in tube_line.service_types:
                tube_line.__setattr__(service_type.lower() + '_routes', routes_dict[service_type])
        return tuple(tube_lines_objects)

    def get_tube_line_stations(self, line_id):
        stations_raw = self.tfl_api_dao.get_single_line_stations(line_id)
        stations = map(TubeStation, stations_raw)
        return stations

    def get_line_route_sequences(self, line_id, service_type):
        line_routes_full_raw = self.tfl_api_dao.get_all_route_station_sequences(line_id, service_type)
        line_routes_dict_list = line_routes_full_raw['orderedLineRoutes']
        routes_dict = defaultdict(list)
        for line_route in line_routes_dict_list:
            line_route['lineId'] = line_routes_full_raw['lineId']
            line_route['lineName'] = line_routes_full_raw['lineName']
            line_route['mode'] = line_routes_full_raw['mode']
            routes_dict[line_route['serviceType']].append(TubeRoute(line_route))
        return routes_dict

    def get_all_tube_stop_points(self):
        tube_stop_points_response = self.tfl_api_dao.get_all_tube_stop_points()
        tube_stop_points_list = tube_stop_points_response['stopPoints']
        return tube_stop_points_list

    def get_tube_stations(self):
        stop_points_raw = self.get_all_tube_stop_points()
        stop_points_by_stop_type = self._arrange_stop_points_by_stop_type(stop_points_raw)
        tube_stations = self._convert_stop_points_dicts_to_tube_stations(stop_points_by_stop_type)
        return tube_stations

    def _convert_stop_points_dicts_to_tube_stations(self, stop_points_by_stop_type_dict):
        tube_stations_dicts = stop_points_by_stop_type_dict['NaptanMetroStation']
        tube_stations = self._create_tube_stations_from_stop_points(tube_stations_dicts)
        return tube_stations

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

