# from django.shortcuts import render
import json
import os
# import requests

from ast import literal_eval

from django.http import HttpResponse
from django.conf import settings
# from django.template import (Template,
#                              # Context,
#                              )

from jinja2 import Template, Environment, FileSystemLoader

from .fhir_interface import f_metadata, f_get, get_all_bundle, f_put
from .formatter import pretty_json, get_template
from ..fhiroperation.arg_handler import get_arg, bool_env

THIS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/profhirler'
URL = settings.FHIR_URL
content_type = 'application/json'
payer_system_old = "https://old.payer.example.com/" \
                   "diamond-health-ppo/uniquemember"
payer_system_new = "https://new.payer.example.com/" \
                   "diamond-health-hmo/uniquemember"
payer_umb_prefix_old = "dh-"
payer_unique_member_code = "MB"


def index(request):
    response = """
    <h1>Welcome to profhirler - the FHIR Handler</h1>

    <p>Base Url: <i>/v1/profhirler/</i></p>

    <p>Commands:</p>
    <li>Metadata</li>
    <li>Coverage?create=True|False</li>
    <li>[Resource Name - Case Sensitive]</li>
    <li>Patient/$member-match</li>
    """

    return HttpResponse(response)


def get_metadata(request):
    """
    get metadata
    :return:
    """
    resource = "metadata"
    result = f_metadata(URL + resource)
    response = pretty_json(result.json(),
                           pretty=True)

    return HttpResponse(response,
                        content_type=content_type)


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
    response = pretty_json(result.json(),
                           pretty=True)

    return HttpResponse(response,
                        content_type=content_type)


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

    result = f_metadata("{url}{resource}/{id}".format(url=URL,
                                                      resource=resource,
                                                      id=_id))
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
    # print("Dir:", THIS_DIR)
    j2_env = Environment(loader=FileSystemLoader(THIS_DIR),
                         trim_blocks=True)
    if j2_env:
        pass
    p = f_metadata(URL + "Patient")
    # response = pretty_json(p.json(), pretty=True)

    # entries = p.json()['entry']
    # print(len(entries))
    # total = 0
    # if 'total' in p.json():
    #     total = p.json()['total']
    # print("total:", total)

    bundle = get_all_bundle(p.json())
    patient_ids = []
    for e in bundle['entry']:
        if 'id' in e['resource']:
            patient_ids.append(e['resource']['id'])
    template_content = str(get_template('patient_identifier.json'))
    # print(template_content)
    # Change each patient record to add umb number
    # print(type(template_content))
    template = Template(template_content)
    # print(type(template))
    ct = 10001
    patient_umbs = []
    new_patients = []
    written_patients = []
    for p in bundle['entry']:
        patient_umb = {"system": payer_system_old,
                       "number": payer_umb_prefix_old + str(ct),
                       "code": payer_unique_member_code}

        added_id = template.render(patient_id=patient_umb)
        # print("Rendered Template Type:", type(added_id))
        # print("Result:\n", added_id)

        add = literal_eval(added_id)
        # print("Add:", type(add))

        if 'identifier' in p['resource']:
            p['resource']['identifier'].append(add)
        else:
            p['resource']['identifier'] = add
            new_patients.append(p['resource'])
        ct += 1
        # print("writing to ", URL + "Patient/" + p['resource']['id'])
        # print("with:\n", p['resource'])
        write_patient = f_put(URL + "Patient/" + p['resource']['id'],
                              data=json.dumps(p['resource']))
        # print(write_patient)
        written_patients.append(write_patient.json())
        patient_umbs.append(added_id)

    return HttpResponse(json.dumps(written_patients,
                                   indent=settings.INDENT),
                        content_type=content_type)


def put_patient(request):
    """
    update a patient
    :param request:
    :return:
    """
    json_source = get_arg(request, 'json_source')
    # print("json_source:", json_source)
    if json_source is None:
        return HttpResponse("no input: ?json_source=filename")

    with open(json_source,
              'r',
              encoding='utf-8-sig') as f:
        r = f.read()
    patient_info = json.loads(r)
    # print(patient_info)
    patient_template_json = get_template('patient.json')
    patient_template_string = Template(json.dumps(patient_template_json))
    patient_to_put = patient_template_string.render(patient=patient_info)

    write_patient = f_put(URL + "Patient/" + str(patient_info['patient_id']),
                          data=patient_to_put)
    return HttpResponse(json.dumps(write_patient.json(),
                                   indent=settings.INDENT),
                        content_type=content_type)


def put_resource(request, resource):
    """
    update a resource
    :param request:
    :param resource:
    :return HttpResponse(json.dumps(result)):
    """

    json_source = get_arg(request, 'json_source')
    # print("json_source:", json_source)
    if json_source is None:
        return HttpResponse("no input: ?json_source=filename")

    with open(json_source,
              'r',
              encoding='utf-8-sig') as f:
        r = f.read()
    if resource.lower() == "coverage":
        coverage_info = json.loads(r)
        patient_info = {}
        key_id = coverage_info['_id']
    else:
        # resource.lower() == "patient":
        coverage_info = {}
        patient_info = json.loads(r)
        key_id = patient_info['_id']

    # print(resource_info)
    resource_template_json = get_template(resource.lower() + '.json')
    resource_template_string = Template(json.dumps(resource_template_json))
    resource_to_put = resource_template_string.render(patient=patient_info,
                                                      coverage=coverage_info)

    write_resource = f_put(URL + resource + "/" + str(key_id),
                           data=resource_to_put)
    return HttpResponse(json.dumps(write_resource.json(),
                                   indent=settings.INDENT),
                        content_type=content_type)
