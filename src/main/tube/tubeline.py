# ^=_ coding: utf-8 _=^

from main.utils import utils


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
