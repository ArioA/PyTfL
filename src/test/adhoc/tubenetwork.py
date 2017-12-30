# ^=_ coding: utf-8 _=^

from tube.tubenetwork import TubeNetwork
from pprint import pprint
import unittest


class TubeNetworkTest(unittest.TestCase):

    def test_tube_network_initialisation(self):
        tube_network = TubeNetwork()
        pprint(tube_network.tube_lines)

    def test_tube_points(self):
        tube_network = TubeNetwork()
        pprint(tube_network.get_tube_stations())


if __name__ == '__main__':
    unittest.main()
