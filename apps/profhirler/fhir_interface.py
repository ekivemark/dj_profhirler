# FHIR Requests handler
#
# author: @ekivemark
#

import requests
from django.conf import settings
# from jsonpath_ng import parser


def f_metadata(url):
    """
    get Metadata
    :param url:
    :return result:
    """

    r = requests.get(url=url)
    # result = {"status": r.status_code, "text": r.text}

    return r


def f_post(url, data={}):
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


def f_put(url, data={}):
    """
    Put / Update a record
    :param url:
    :param data:
    :return result:
    """
    print("DATA is:", type(data))
    r = requests.put(url=url,
                     data=data,
                     headers={
                         'content-type': settings.FHIR_DEFAULT_CONTENT_TYPE})

    return r


def f_get(url, data={}, payload={}):
    """
    Get a record
    :param url:
    :param data:
    :return result:
    """
    r = requests.get(url=url, data=data, params=payload)

    return r


def f_delete(url, data={}):
    """
    Delete records using id
    :param url:
    :param data:
    :return result:
    """

    r = requests.delete(url=url, data=data)
    result = {"status": r.status_code, "text": r.text}
    return result


def get_all_bundle(bundle):
    """
    Compile entries into a single bundle
    :param bundle:
    :return big_bundle:
    """

    # get entry
    entries = bundle['entry']
    total = bundle['total']

    while len(entries) < total:
        # print(len(entries))
        next = get_next_url(bundle['link'])
        if next:
            b = f_metadata(next)
            bundle = b.json()
        entries.extend(bundle['entry'])

    big_bundle = bundle
    big_bundle['entry'] = entries
    return big_bundle


def get_next_url(link):
    """
    get next url
    :param link:
    :return:
    """

    for l in link:
        if l['relation'] == 'next':
            return l['url']

    return None
