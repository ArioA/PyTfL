# ^=_ coding: utf-8 _=^

from pytfl.utils import logging
from pytfl.dao.tubedao import TubeDao

logger = logging.getLogger(__name__)


class TubeNetwork:
    def __init__(self):
        self.dao = TubeDao()
        self.tube_lines = self.dao.get_all_tube_lines()
