import json
import os
from django.conf import settings

THIS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/profhirler/"


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


def get_template(t_name):
    """
    Get template
    :param t_name:
    :return template:
    """
    with open(THIS_DIR + '/templates/' + t_name, 'r', encoding='utf-8-sig') as f:
        r = f.read()
    template = json.loads(r)
    return template
