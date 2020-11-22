# ^=_ coding: utf-8 _=^
import html

from pytfl import utils


class TubeRoute:
    def __init__(self, tuberoute_dict, **kwargs):
        self._raw = tuberoute_dict

        initialising_dict = utils.create_initialising_dict(tuberoute_dict, kwargs)
        self.name = html.unescape(initialising_dict["name"])
        self.station_id_route_sequence = initialising_dict["naptanIds"]
        self.service_type = initialising_dict["serviceType"]
        self.line_id = initialising_dict["lineId"]
        self.line_name = initialising_dict["lineName"]
        self.mode = initialising_dict["mode"]

    def __str__(self):
        return f"<TubeRoute: {self.name}>"

    def __repr__(self):
        return (
            f"TubeRoute(name={self.name}, "
            f"station_id_route_sequence={self.station_id_route_sequence}, "
            f"service_type={self.service_type}, "
            f"line_id={self.line_id}, "
            f"line_name={self.line_name}, "
            f"mode={self.mode})"
        )

    def __len__(self):
        return len(self.station_id_route_sequence)

    def __getitem__(self, item):
        return self.station_id_route_sequence[item]
