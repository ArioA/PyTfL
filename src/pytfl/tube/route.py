# ^=_ coding: utf-8 _=^
import html
from utils import utils


class TubeRoute(object):

    def __init__(self, tuberoute_dict, **kwargs):
        initialising_dict = utils.create_initialising_dict(tuberoute_dict, kwargs)
        self.name = html.unescape(initialising_dict['name'])
        self.station_id_route_sequence = initialising_dict['naptanIds']
        self.service_type = initialising_dict['serviceType']
        self.line_id = initialising_dict['lineId']
        self.line_name = initialising_dict['lineName']
        self.mode = initialising_dict['mode']

    def __str__(self):
        return self.name

    def __repr__(self):
        repr_str_format = 'TubeRoute(name={name}, ' \
                          'station_id_route_sequence={station_id_route_sequence}, ' \
                          'service_type={service_type}, ' \
                          'line_id={line_id}, ' \
                          'line_name={line_name}, ' \
                          'mode={mode})'
        repr_str = repr_str_format.format(name=self.name,
                                          station_id_route_sequence=self.station_id_route_sequence,
                                          service_type=self.service_type,
                                          line_id=self.line_id,
                                          line_name=self.line_name,
                                          mode=self.mode)
        return repr_str

    def __len__(self):
        return len(self.station_id_route_sequence)

    def __getitem__(self, item):
        return self.station_id_route_sequence[item]
