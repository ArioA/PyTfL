# ^=_ coding: utf-8 _=^

from collections import defaultdict
from tube.tubeline import TubeLine
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
        stop_type_to_stop_point = defaultdict(list)
        for stop_point in tube_stop_points_list:
            stop_type = stop_point['stopType']
            stop_type_to_stop_point[stop_type].append(stop_point)
        return dict(stop_type_to_stop_point)
