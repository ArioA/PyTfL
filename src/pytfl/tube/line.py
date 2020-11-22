# ^=_ coding: utf-8 _=^
from pytfl import utils


class TubeLine:
    def __init__(self, tubeline_dict, **kwargs):
        initialising_dict = utils.create_initialising_dict(tubeline_dict, kwargs)

        self.name = initialising_dict["name"]
        self.id = initialising_dict["id"]
        self.line_statuses = initialising_dict["lineStatuses"]
        self.disruptions = initialising_dict["disruptions"]
        self.service_types = self.get_service_type(initialising_dict["serviceTypes"])
        self.mode_name = initialising_dict.get("modeName", "tube")
        self.tube_stations = []
        self.regular_routes = []
        self.night_routes = []

    @staticmethod
    def get_service_type(service_types):
        return tuple(service_type["name"] for service_type in service_types)

    def __str__(self):
        return f"<TubeLine: {self.name}>"

    def __repr__(self):
        return (
            f"TubeLine(name={self.name}, "
            f"id={self.id,}, "
            f"tube_stations={self.tube_stations}, "
            f"regular_routes={self.regular_routes}, "
            f"night_routes={self.night_routes}, "
            f"line_statuses={self.line_statuses}, "
            f"disruptions={self.disruptions}, "
            f"service_types={self.service_types}, "
            f"mode_name={self.mode_name})"
        )
