# ^=_ coding: utf-8 _=^

from utils import utils


class TubeLine(object):

    def __init__(self, tubeline_dict, **kwargs):
        if isinstance(tubeline_dict, dict):
            initialising_dict = tubeline_dict
        else:
            initialising_dict = kwargs

        self.name = initialising_dict['name']
        self.id = initialising_dict['id']
        self.line_statuses = initialising_dict['lineStatuses']
        self.disruptions = initialising_dict['disruptions']
        self.service_types = self.get_service_type(initialising_dict['serviceTypes'])
        self.mode_name = initialising_dict.get('modeName', 'tube')

    @staticmethod
    def get_service_type(service_types):
        name_getter = utils.create_dict_getter('name')
        service_type_names = map(name_getter, service_types)
        return tuple(service_type_names)

    def __str__(self):
        return self.name

    def __repr__(self):
        repr_str_format = 'TubeLine(name={name}, ' \
                          'id={id}, ' \
                          'line_statuses={line_statuses}, ' \
                          'disruptions={disruptions}, ' \
                          'service_types={service_types}, ' \
                          'mode_name={mode_name})'
        repr_str = repr_str_format.format(name=self.name,
                                          id=self.id,
                                          line_statuses=self.line_statuses,
                                          disruptions=self.disruptions,
                                          service_types=self.service_types,
                                          mode_name=self.mode_name)
        return repr_str
