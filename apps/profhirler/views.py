# from django.shortcuts import render
import json
import requests

from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.template import Template, Context

from .fhir_interface import f_metadata, f_get, get_all_bundle, f_put
from .formatter import pretty_json, get_template
from ..fhiroperation.arg_handler import get_arg, bool_env

URL = settings.FHIR_URL
content_type = 'application/json'
payer_system_old = "https://old.payer.example.com/diamond-health-ppo/uniquemember"
payer_system_new = "https://new.payer.example.com/diamond-health-hmo/uniquemember"
payer_umb_prefix_old = "dh-"
payer_unique_member_code = "UMB"

def index(request):
    response = """
    <h1>Welcome to profhirler - the FHIR Handler</h1>
    
    <p>Base Url: <i>/v1/profhirler/</i></p>
    
    <p>Commands:</p>
    <li>Metadata</li>
    <li>Coverage?create=True|False</li>
    <li>[Resource Name - Case Sensitive]</li>
        
    """

    return HttpResponse(response)

def get_metadata(request):
    """
    get metadata
    :return:
    """
    resource = "metadata"
    result = f_metadata(URL + resource)
    response = pretty_json(result.json(), pretty=True)

    return HttpResponse(response, content_type=content_type)


def get_coverage(request):
    """
    Handle the coverage resource

    :param request:
    :return response:
    """
    create = bool_env(get_arg(request, 'create'))

    if create:
        print("Create operation")

        # Add create record processing here
        response = "result of Create"
        return HttpResponse(response)

    # get coverage records
    resource = "Coverage"
    result = f_get(URL + resource)
    response = pretty_json(result.json(), pretty=True)

    return HttpResponse(response, content_type=content_type)


def get_resource(request, resource):
    """
    Handle any resource

    :param request:
    :param resource:
    :return response:
    """

    create = bool_env(get_arg(request, 'create'))

    if create:
        print("Create operation for ", resource)

        # Add create record processing here
        response = "result of Create for " + resource
        return HttpResponse(response)

    # get coverage records

    result = f_metadata(URL + resource)
    response = pretty_json(result.json(), pretty=True)

    return HttpResponse(response, content_type=content_type)


def get_resource_id(request, resource, _id):
    """
    Handle any resource request for a specific id

    :param request:
    :param resource:
    :param _id:
    :return response:
    """

    create = bool_env(get_arg(request, 'create'))

    if create:
        print("Create operation for ", resource)

        # Add create record processing here
        response = "result of Create for " + resource
        return HttpResponse(response)

    # get coverage records

    result = f_metadata("{url}{resource}/{id}".format(url=URL, resource=resource, id=_id))
    response = pretty_json(result.json(), pretty=True)

    return HttpResponse(response, content_type=content_type)


def change_patient(request):
    """
    Get patient bundle
    Add UMB to each Patient record
    write updated Patient record
    :param request:
    :return:
    """

    p = f_metadata(URL + "Patient")
    response = pretty_json(p.json(), pretty=True)

    entries = p.json()['entry']
    print(len(entries))
    total = 0
    if 'total' in p.json():
        total = p.json()['total']
    print("total:", total)

    bundle = get_all_bundle(p.json())
    patient_ids = []
    for e in bundle['entry']:
        if 'id' in e['resource']:
            patient_ids.append(e['resource']['id'])

    # Change each patient record to add umb number
    template = Template(get_template('patient_identifier.json'))
    print(type(template))
    ct = 10001
    patient_umbs = []
    for p in bundle['entry']:
        patient_umb = {"system": payer_system_old,
                       "number": payer_umb_prefix_old + str(ct),
                       "code": payer_unique_member_code}
        context = Context({'patient_id': patient_umb})

        added_id = template.render(context)
        print(type(added_id))
        print(added_id)
        if 'identifier' in p['resource']:
            p['resource']['identifier'].append(added_id)
        else:
            p['resource']['identifier'] = added_id
        ct += 1
        write_patient = f_put(URL + "Patient/" + p['resource']['id'])
        patient_umbs.append(added_id)

    return HttpResponse(patient_umbs, content_type=content_type)
