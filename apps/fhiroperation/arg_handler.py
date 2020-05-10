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
