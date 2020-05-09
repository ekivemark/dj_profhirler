# from django.shortcuts import render
import json

from django.http import HttpResponse, JsonResponse
from django.conf import settings

from .fhir_interface import f_metadata
from .formatter import pretty_json

URL = settings.FHIR_URL
content_type = 'application/json'

def index(request):
    response = """
    <h1>Welcome to profhirler - the FHIR Handler</h1>
    
    <p>Base Url: <i>/v1/profhirler/</i></p>
    
    <p>Commands:</p>
    <li>Metadata</li>
    <li>CapabilityStatement</li>
        
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


