import json
from django.conf import settings

def pretty_json(output, pretty=False):
    """
    Make json output pretty
    :param output:
    :param pretty:
    :return output:
    """

    if pretty:
        return json.dumps(output, indent=settings.INDENT)
    else:
        return output
