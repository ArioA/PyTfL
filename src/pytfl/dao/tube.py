# ^=_ coding: utf-8 _=^
from collections import defaultdict, abc
from typing import List

from pytfl.dao.tfl_api_dao import TflApiDao
from pytfl.tube.line import TubeLine
from pytfl.tube.station import TubeStation
from pytfl.tube.route import TubeRoute
from pytfl.utils import logging

logger = logging.getLogger(__name__)


def line_name_to_attr(line: str) -> str:
    return line.replace(" & ", "_").lower()


# TODO: have an explicit list of lines
class TubeLines(abc.Sequence):
    """
    Class representing all tube lines:

    >>> tubelines = Tube().lines
    >>> northern_line = tubelines.northern
    """

    def __init__(self, tubelines: List[TubeLine]):
        self._tubelines = tubelines
        for line in tubelines:
            attr = line_name_to_attr(line.name)
            setattr(self, attr, line)

    def __len__(self):
        return len(self._tubelines)

    def __getitem__(self, item):
        return self._tubelines[item]


class Tube:
    def __init__(self):
        self.tfl_api_dao = TflApiDao()

    @property
    def lines(self) -> TubeLines:
        tube_lines_raw = (
            self.tfl_api_dao.get_all_tube_lines()
        )  # TODO: Call Lines/Mode/tube/Status instead of Line/Mode/tube - the latter is rubbish
        tube_lines_objects = [TubeLine(tube_line_dict) for tube_line_dict in tube_lines_raw]
        return TubeLines(tube_lines_objects)

    def get_all_tube_lines(self):
        tubelines = self.lines
        for tube_line in tubelines:
            stations = self.get_tube_line_stations(tube_line.id)
            tube_line.tube_stations = tuple(stations)
            routes_dict = self.get_line_route_sequences(tube_line.id, "Regular,Night")
            for service_type in tube_line.service_types:
                setattr(tube_line, f"{service_type.lower()}_routes", routes_dict[service_type])
        logger.info("Got %s tube lines from TfL.", len(tubelines))
        return tubelines

    def get_tube_line_stations(self, line_id):
        logger.info("Getting all stations for tube line with ID: %s", line_id)
        stations_raw = self.tfl_api_dao.get_single_line_stations(line_id)
        stations = [TubeStation(station) for station in stations_raw]
        logger.info("Got %s stations for tube line with ID: %s", len(stations), line_id)
        return stations

    def get_line_route_sequences(self, line_id, service_type):
        logger.info(
            "Getting all routes for line ID: %s and service type(s): %s", line_id, service_type
        )
        line_routes_full_raw = self.tfl_api_dao.get_all_route_station_sequences(
            line_id, service_type
        )
        line_routes_dict_list = line_routes_full_raw["orderedLineRoutes"]
        logger.info("Got %s routes for station id: %s", len(line_routes_dict_list), line_id)
        routes_dict = defaultdict(list)
        for line_route in line_routes_dict_list:
            line_route["lineId"] = line_routes_full_raw["lineId"]
            line_route["lineName"] = line_routes_full_raw["lineName"]
            line_route["mode"] = line_routes_full_raw["mode"]
            routes_dict[line_route["serviceType"]].append(TubeRoute(line_route))
        logger.info("Got routes for line ID: %s and service type(s): %s", line_id, service_type)
        return routes_dict

    def get_all_tube_stop_points(self):
        logger.info("Getting all tube stop points.")
        tube_stop_points_response = self.tfl_api_dao.get_all_tube_stop_points()
        tube_stop_points_list = tube_stop_points_response["stopPoints"]
        logger.info("Got %s tube stop points", len(tube_stop_points_list))
        return tube_stop_points_list

    def get_tube_stations(self):
        logger.info("Getting all tube stations.")
        stop_points_raw = self.get_all_tube_stop_points()
        stop_points_by_stop_type = self._arrange_stop_points_by_stop_type(stop_points_raw)
        tube_stations = self._convert_stop_points_dicts_to_tube_stations(stop_points_by_stop_type)
        logger.info("Got %s tube stations", len(tube_stations))
        return tube_stations

    def _convert_stop_points_dicts_to_tube_stations(self, stop_points_by_stop_type_dict):
        tube_stations_dicts = stop_points_by_stop_type_dict["NaptanMetroStation"]
        tube_stations = self._create_tube_stations_from_stop_points(tube_stations_dicts)
        return tube_stations

    @staticmethod
    def _arrange_stop_points_by_stop_type(tube_stop_points_list):
        stop_type_to_stop_point = defaultdict(list)
        for stop_point in tube_stop_points_list:
            stop_type = stop_point["stopType"]
            stop_type_to_stop_point[stop_type].append(stop_point)
        return dict(stop_type_to_stop_point)

    @staticmethod
    def _create_tube_stations_from_stop_points(tube_stations_dict_list):
        tube_stations = map(TubeStation, tube_stations_dict_list)
        return tuple(tube_stations)
