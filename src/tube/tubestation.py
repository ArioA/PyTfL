# ^=_ coding: utf-8 _=^


class TubeStation(object):

    def __init__(self, tube_station_dict, **kwargs):
        if isinstance(tube_station_dict, dict):
            initialising_dict = tube_station_dict
        else:
            initialising_dict = kwargs

        self.name = initialising_dict['commonName']
        self.id = initialising_dict['id']
        self.lat = initialising_dict['lat']
        self.lon = initialising_dict['lon']
        self.naptan_stop_type = initialising_dict['stopType']
        self.additional_properties = []  # TODO: add additionalProperties key
        self.children = []  # TODO: add children

    def __str__(self):
        return self.name

    def __repr__(self):
        repr_str_format = 'TubeStation(name={name}, ' \
                          'id={id}, ' \
                          'lat={lat}, ' \
                          'lon={lon}, ' \
                          'naptan_stop_type={naptan_stop_type}, ' \
                          'additional_properties={additional_properties}, ' \
                          'children={children})'
        repr_str = repr_str_format.format(name=self.name,
                                          id=self.id,
                                          lat=self.lat,
                                          lon=self.lon,
                                          naptan_stop_type=self.naptan_stop_type,
                                          additional_properties=self.additional_properties,
                                          children=self.children)
        return repr_str
