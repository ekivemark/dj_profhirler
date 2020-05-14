# from django.shortcuts import render
import json
import os

from django.http import HttpResponse, JsonResponse
from django.conf import settings
# from django.template.loader import render_to_string

# from ..profhirler.fhir_interface import f_metadata
from ..profhirler.fhir_interface import f_get
# from ..profhirler.formatter import pretty_json
from .arg_handler import (get_arg,
                          extract_values,
                          extract_object,
                          join_related_lists
                          )

THIS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) \
           + "/fhiroperation/"
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
    :param request:
    :return result_parameter:
    """
    # operation = "$member-match"
    sample_return = bool(get_arg(request, 'sample_return'))
    # = True
    # print("Sample Return:", sample_return)
    if sample_return:
        # return a sample parameter response
        with open(THIS_DIR + '/templates/parameter_response.json',
                  'r',
                  encoding='utf-8-sig') as f:
            r = f.read()
        response = json.loads(r)
        return HttpResponse(json.dumps(response,
                                       indent=settings.INDENT),
                            content_type=content_type)
    # We didn't do a sample return so now we will process a member-match
    if request.method == "GET":
        if request.content_type in ['application/json',
                                    'application/json+fhir']:
            member = {}
            coverage = {}
            requester = {}
            beneficiary = {}
            parameters_out = {"resourceType": "Parameters",
                              "parameter": []
                              }
            unique_id = {"name": "uniqueMemberId",
                         "identifier": []
                         }

            mm_input = json.loads(request.read())
            if 'parameter' in mm_input:
                print("How many parameters:", len(mm_input['parameter']))
                for param in mm_input['parameter']:
                    if 'name' in param:
                        if param['name'].lower() == "memberpatient":
                            member = param['resource']
                            print("Member:", member['name'])
                        elif param['name'].lower() == "oldcoverage":
                            coverage = param['resource']

                        elif param['name'].lower() == "newcoverage":
                            requester = param['resource']
                            print("Requester:", requester)

            if coverage:
                # get coverage info and search for unique records
                if 'identifier' in coverage:
                    print("coverage identifier:", coverage['identifier'])
                    ident_search = coverage['identifier'][0]['value']
                    search_payload = {'identifier': ident_search}
                    resource = "Coverage"

                    plan_coverage = f_get(URL + resource,
                                          data={},
                                          payload=search_payload)

                    # next we need to check the coverage records
                    # print(plan_coverage)
                    result_coverage = plan_coverage.json()
                    coverage_count = result_coverage['total']
                    if coverage_count == 0:
                        return JsonResponse({"error": "member id not found"},
                                            status=settings.MEMBER_MATCH_NOT_FOUND)
                    if coverage_count > 1:
                        return JsonResponse({"error": "unique member id not found"},
                                            status=settings.MEMBER_MATCH_NOT_FOUND)
                    # Only return information if there is a unique coverage record found.
                    print("Coverages=", coverage_count)

                    # Get patient record for the coverage
                    if 'entry' in result_coverage:
                        print("Result:", result_coverage)
                        beneficiary_ref = extract_object(result_coverage, 'beneficiary')
                        print("Bene Ref:", beneficiary_ref)
                        if len(beneficiary_ref) > 0 and 'reference' in beneficiary_ref[0]:
                            print(URL + beneficiary_ref[0]['reference'])
                            beneficiary = f_get(URL + beneficiary_ref[0]['reference'])

                    # Update the received Patient Record by adding the new identifier.
                    print("Beneficiary:", beneficiary.json())
                    beneficiary_identifier = extract_object(beneficiary.json(), 'identifier')
                    code_type = extract_values(beneficiary_identifier, 'code')
                    code_value = extract_values(beneficiary_identifier, 'value')
                    identifier_cv = join_related_lists(code_type, code_value)
                    print("Codes and Values:", identifier_cv)
                    print("bene id:", beneficiary_identifier)

                    if "UMB" in identifier_cv:
                        for id in beneficiary_identifier[0]:
                            if id['type']['coding'][0]['code'].upper() == "UMB":
                                member['identifier'].append(id)
                                unique_id['identifier'].append(id)

                    # Return the updated patient record
                    # after it is wrapped back into a parameters resource
                    if member:
                        parameters_out['parameter'].append({"name": "MemberPatient",
                                                            "resource": member})
                    if requester:
                        parameters_out['parameter'].append({"name": "NewCoverage",
                                                            "resource": requester})
                    if len(unique_id['identifier']) > 0:
                        parameters_out['parameter'].append(unique_id)

                    return HttpResponse(json.dumps(parameters_out))

            return HttpResponse(json.dumps(parameters_out))

    return ("Houston. We have a problem")
