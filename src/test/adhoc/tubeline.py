# ^=_ coding: utf-8 _=^

import unittest
from utils.tfl_http import TflHttp
from pprint import pprint


class TubeLineTest(unittest.TestCase):

    def test_get_all_tube_lines(self):
        tfl_http = TflHttp()
        all_tube_lines = tfl_http.get_all_tube_lines()
        pprint(all_tube_lines)


if __name__ == '__main__':
    unittest.main()
