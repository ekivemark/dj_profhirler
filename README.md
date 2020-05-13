# dj_profhirler

This is an alpha toolkit that enables FHIR resources to be created via Jinja2 templates.
It was created to enable easy editing of FHIR resources for the FHIR connectathon, May 2020.

This python/django app can be run locally and pointed at an open HL7 FHIR server.

Resources can be read from the FHIR Server.

## Create a resource using a template:

    [base]/v1/profhirler/{resource}/put?json_source=file.name 

- Create a json template in apps/profhirler/templates that matches the resource name.
- Insert replaceable parameters into the template
- Define the replaceable parameters in the .json file that is referenced in ?json_source

## Search and GET

    [base]/v1/profhirler/{resource}/{id}?{query_params}
    

## Patient/$member-match

A reference implementation for a Payer-to-payer member-match operation is included.

Submit a parameters resource to the operation using the body of a GET to:

    [base]/v1/profhirler/Patient/$member-match
    
## Installation

    install python3.8
    # create virtual environment
    python3.8 -m venv v_env
    # activate virtual environment
    source v_env/bin/activate
    # install package dependencies
    pip install -r requirements.txt
    # initialize django and database
    python manage.py migrate
    # run server on default port 8000
    python manage.py runserver

Open a browser and goto

    http://localhost:8000/v1/profhirler




--- 
File: README.md
Date: 5/13/20
Author: @ekivemark
