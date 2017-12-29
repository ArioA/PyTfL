# ^=_ coding: utf-8 _=^


def create_dict_getter(key):
    def dict_getter(a_dict):
        return a_dict[key]

    return dict_getter
