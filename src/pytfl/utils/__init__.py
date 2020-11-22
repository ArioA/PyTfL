# ^=_ coding: utf-8 _=^


def create_dict_getter(key):
    def dict_getter(a_dict):
        return a_dict[key]

    return dict_getter


def create_initialising_dict(api_dict, kwargs_dict):
    """
    Used so that the kwargs override whatever data is in api_dict when initialising an object.

    Parameters
    ----------
    api_dict: dict
        A dict returned by TfL's API which can be used to initialise an object (e.g. TubeStation)

    kwargs_dict: dict
        Dictionary of the key-word arguments passed to a class' initialiser.

    Returns
    -------
    dict
        A dictionary of values to be used to initialise a class. The values are such that the values present in
        kwargs_dict override those found in api_dict.
    """
    return {**api_dict, **kwargs_dict}
