# FHIR Requests handler
#
# author: @ekivemark
#

import requests
from django.conf import settings


def f_metadata(url):
    """
    get Metadata
    :param url:
    :return result:
    """

    r = requests.get(url=url)
    # result = {"status": r.status_code, "text": r.text}

    return r


def f_post(url, data):
    """
    Post data to url
    :param url:
    :param data:
    :return: result
    """

    r = requests.post(url=url, data=data)

    # print(r.json)

    result = {"status": r.status_code, "text": r.text}

    return result


def f_put(url, data):
    """
    Put / Update a record
    :param url:
    :param data:
    :return result:
    """
    r = requests.put(url=url, data=data)

    # print(r.json)

    result = {"status": r.status_code, "text": r.text}

    return result


def f_get(url, data):
    """
    Get a record
    :param url:
    :param data:
    :return result:
    """
    r = requests.get(url=url, data=data)
    result = {"status": r.status_code, "text": r.text}
    return result


def f_delete(url, data):
    """
    Delete records using id
    :param url:
    :param data:
    :return result:
    """

    r = requests.delete(url=url, data=data)
    result = {"status": r.status_code, "text": r.text}
    return result
