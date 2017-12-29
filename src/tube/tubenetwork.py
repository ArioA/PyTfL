# ^=_ coding: utf-8 _=^

from tube.tubeline import TubeLine
from utils.tfl_http import TflHttp


class TubeNetwork(object):

    def __init__(self):
        self.api_communicator = TflHttp()
        self.tube_lines = self.create_tube_lines()

    def create_tube_lines(self):
        tube_lines_raw = self.api_communicator.get_all_tube_lines()
        tube_lines_objects = map(TubeLine, tube_lines_raw)
        return tuple(tube_lines_objects)
