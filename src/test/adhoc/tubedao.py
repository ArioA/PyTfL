# ^=_ coding: utf-8 _=^

from dao.tubedao import TubeDao
from pprint import pprint
import unittest


class TubeDaoTest(unittest.TestCase):

    def setUp(self):
        self.dao = TubeDao()

    def test_tube_points(self):
        pprint(self.dao.get_tube_stations())

    def test_get_all_tube_lines(self):
        all_tube_lines = self.dao.get_all_tube_lines()
        pprint(all_tube_lines)


if __name__ == '__main__':
    unittest.main()
