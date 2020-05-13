# Arg_handler
# Author: @ekivemark
#

TRUE_LIST = [1, "1", "true", "True", "TRUE", "YES", "Yes", "yes", True]
FALSE_LIST = [0, "0", "False", "FALSE", "false", "NO", "No", "no", False]


def get_arg(request, qp=None):
    """
    Get args from request.query_params
    :param request:
    :param qp:
    :return arg:
    """

    if qp:
        query = request.GET.get(qp, None)
        return query
    else:
        return None


def bool_env(env_val):
    """ check for boolean values """

    if env_val:
        if env_val in TRUE_LIST:
            return True
        if env_val in FALSE_LIST:
            return False
        return env_val
    else:
        if env_val in FALSE_LIST:
            return False
        return


def coverage_type(coverage_identifier, csys=None, ctype=None):
    """
    look for coverage type (ctype) in coverage_identifier,
    return list item with ctype
    :param coverage_identifier:
    :param ctype:
    :return coverage_value:
    """
    # if ctype is None:
    #     return None
    # cval = []
    # if coverage_identifier:
    #     for ci in coverage_identifier:
    #         if csys:
    #             if 'system' in ci:
    #                 if ci['system'] == csys:
    #                     cval.append()
    #         if 'type' in ci:
    #             if ci['type'] == ctype
    return


def extract_values(obj, key):
    """
    Pull all values of specified key from nested JSON.
    Great code snippet from Todd Birchard via
    https://hackersandslackers.com/extract-data-from-complex-json-python/

    """
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    results = extract(obj, arr, key)
    return results


def join_related_lists(list_key=[], list_value=[]):
    """
    Connect two related lists. First list becomes the key,
    The second the values

    :param list_key:
    :param list_value:
    :return joined_dict:
    """

    joined_dict = dict(zip(list_key, list_value))
    return joined_dict


def extract_object(obj, key):
    """
    Pull all list or dict with specified key from nested JSON.
    Based on a great code snippet from Todd Birchard via
    https://hackersandslackers.com/extract-data-from-complex-json-python/

    """
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k == key:
                    arr.append(v)
                elif isinstance(v, (dict, list)):
                    extract(v, arr, key)
        elif isinstance(obj, list):
            for item in obj:
                if item == key:
                    arr.append(item)
                else:
                    extract(item, arr, key)
        return arr

    results = extract(obj, arr, key)
    return results
