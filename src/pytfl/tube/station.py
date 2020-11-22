# ^=_ coding: utf-8 _=^
from pytfl import utils


class TubeStation:
    def __init__(self, tube_station_dict, **kwargs):
        self._raw = tube_station_dict
        initialising_dict = utils.create_initialising_dict(tube_station_dict, kwargs)

        self.name = initialising_dict["commonName"]
        self.id = initialising_dict["id"]
        self.lat = initialising_dict["lat"]
        self.lon = initialising_dict["lon"]
        self.naptan_stop_type = initialising_dict["stopType"]
        self.additional_properties = []  # TODO: add additionalProperties key
        self.children = []  # TODO: add children

    def __str__(self):
        return f"<TubeStation: {self.name}>"

    def __repr__(self):
        return (
            f"TubeStation(name={self.name}, "
            f"id={self.id}, "
            f"lat={self.lat}, "
            f"lon={self.lon}, "
            f"naptan_stop_type={self.naptan_stop_type}, "
            f"additional_properties={self.additional_properties}, "
            f"children={self.children})"
        )
