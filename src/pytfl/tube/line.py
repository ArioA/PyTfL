# ^=_ coding: utf-8 _=^
import dataclasses
from datetime import datetime
from typing import List, NamedTuple, Optional

from pytfl import utils
from pytfl.dao.tfl_api_dao import TflApiDao
from pytfl.tube.station import TubeStation

DT_FMT = "%Y-%m-%dT%H:%M:%S%z"


@dataclasses.dataclass(frozen=True)
class LineDisruption:
    category: str
    category_description: str
    description: str
    created_at: Optional[datetime]

    @classmethod
    def from_api_response(cls, response: dict):
        return cls(
            category=response["category"],
            category_description=response["categoryDescription"],
            description=response["description"],
            created_at=datetime.strptime(response["created"], DT_FMT)
            if "created" in response
            else None,
        )


class ValidityPeriod(NamedTuple):
    start: datetime
    end: datetime

    @classmethod
    def from_api_response(cls, response: dict):
        return cls(
            start=datetime.strptime(response["fromDate"], DT_FMT),
            end=datetime.strptime(response["toDate"], DT_FMT),
            # isNow key return bad data - `False` when is in fact now.
        )


@dataclasses.dataclass(frozen=True)
class LineStatus:
    status_code: int
    description: str
    reason: Optional[str]
    validity_periods: List[ValidityPeriod]
    disruption: Optional[LineDisruption]

    @classmethod
    def from_api_response(cls, response: dict) -> "LineStatus":
        return cls(
            status_code=response["statusSeverity"],
            description=response["statusSeverityDescription"],
            reason=response.get("reason"),
            validity_periods=[
                ValidityPeriod.from_api_response(period)
                for period in response.get("validityPeriods", [])
            ],
            disruption=LineDisruption.from_api_response(response["disruption"])
            if "disruption" in response
            else None,
        )


class TubeLine:
    def __init__(self, tubeline_dict, **kwargs):
        self._raw = tubeline_dict
        initialising_dict = utils.create_initialising_dict(tubeline_dict, kwargs)

        self.name = initialising_dict["name"]
        self.id = initialising_dict["id"]
        # Deprecated value? Seems to always return [] despite disruptions. Use statuses instead.
        self.disruptions = initialising_dict["disruptions"]
        self.service_types = self.get_service_type(initialising_dict["serviceTypes"])
        self.mode_name = initialising_dict.get("modeName", "tube")
        # TODO
        self.regular_routes = []
        self.night_routes = []

        self._statuses = None
        self._stations = None

    @property
    def statuses(self):
        if self._statuses is None:
            self.refresh_statuses()
        return self._statuses

    @property
    def stations(self):
        if self._stations is None:
            dao = TflApiDao()
            self._stations = [
                TubeStation(raw_station) for raw_station in dao.get_single_line_stations(self.id)
            ]
        return self._stations

    def refresh_statuses(self):
        self._statuses = self._get_statuses()

    def _get_statuses(self) -> List[LineStatus]:
        dao = TflApiDao()
        raw_statuses = dao.get_line_status(self.id)[0]["lineStatuses"]
        return [LineStatus.from_api_response(raw_status) for raw_status in raw_statuses]

    @staticmethod
    def get_service_type(service_types):
        return tuple(service_type["name"] for service_type in service_types)

    def __str__(self):
        return f"<TubeLine: {self.name}>"

    def __repr__(self):
        return (
            f"TubeLine(name={self.name}, "
            f"id={self.id}, "
            f"tube_stations={self.tube_stations}, "
            f"regular_routes={self.regular_routes}, "
            f"night_routes={self.night_routes}, "
            f"statuses={self.statuses}, "
            f"disruptions={self.disruptions}, "
            f"service_types={self.service_types}, "
            f"mode_name={self.mode_name})"
        )
