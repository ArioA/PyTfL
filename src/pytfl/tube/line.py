# ^=_ coding: utf-8 _=^
import dataclasses
from datetime import datetime
from typing import List, NamedTuple

from pytfl import utils
from pytfl.dao.tfl_api_dao import TflApiDao

@dataclasses.dataclass(frozen=True)
class LineDisruption:
    category: str
    category_description: str
    description: str
    created_at: datetime


class ValidityPeriod(NamedTuple):
    start: datetime
    end: datetime


@dataclasses.dataclass(frozen=True)
class LineStatus:
    status_code: int
    description: str
    reason: str
    validity_periods: List[ValidityPeriod]
    disruption: LineDisruption


class TubeLine:
    def __init__(self, tubeline_dict, **kwargs):
        self._raw = tubeline_dict
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

        self._statuses = None

    @property
    def statuses(self):
        if self._statuses is None:
            self.refresh_statuses()
        return self._statuses

    def refresh_statuses(self):
        self._statuses = self._get_statuses()

    def _get_statuses(self) -> List[LineStatus]:
        dao = TflApiDao()


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
