# from django.shortcuts import render
import json
import os

from django.http import HttpResponse, JsonResponse
from django.conf import settings

# from ..profhirler.fhir_interface import f_metadata
# from ..profhirler.formatter import pretty_json

THIS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/fhiroperation/"
URL = settings.FHIR_URL
content_type = 'application/json'

def index(request):
    response = """
    <h1>FHIR Operations Handlers</h1>
    
    <p>Base Url: <i>/v1/profhirler/Patient/</i></p>
    
    <p>Commands:</p>
    <li>$member-match</li>
        
    """

    return HttpResponse(response)

def get_membermatch(request):
    """
    $member-match
    FHIR Operation for a Payer-to-Payer match for member
    receives Parameter bundle
    returns Parameter bundle
    :param parameters:
    :return result_parameter:
    """
    operation = "$member-match"
    # resource = "metadata"
    # result = f_metadata(URL + resource)
    # response = pretty_json(result.json(), pretty=True)
    with open(THIS_DIR + '/templates/parameter_response.json', 'r', encoding='utf-8-sig') as f:
        r = f.read()

    response = json.loads(r)

    return HttpResponse(json.dumps(response, indent=settings.INDENT), content_type=content_type)


