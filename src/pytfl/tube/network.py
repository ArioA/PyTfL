# ^=_ coding: utf-8 _=^

from utils import logging
from dao.tubedao import TubeDao

logger = logging.getLogger(__name__)


class TubeNetwork(object):
    def __init__(self):
        self.dao = TubeDao()
        self.tube_lines = self.dao.get_all_tube_lines()
