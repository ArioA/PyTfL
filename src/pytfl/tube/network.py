# ^=_ coding: utf-8 _=^

from pytfl.utils import logging
from pytfl.dao.tubedao import Tube

logger = logging.getLogger(__name__)


class TubeNetwork:
    def __init__(self):
        self.tube = Tube()
        self.tube_lines = self.tube.get_all_tube_lines()
