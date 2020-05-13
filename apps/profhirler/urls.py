"""
profhirler views

"""
from django.urls import path

from . import views
from ..fhiroperation import views as operation_views

urlpatterns = [
    path('UpdatePatient', views.change_patient, name="change_patient"),
    path('Metadata', views.get_metadata, name='metadata'),
    path('Patient/$member-match', operation_views.get_membermatch, name='member_match'),
    path('<resource>/put', views.put_resource, name='put_resource'),
    path('<resource>/<_id>', views.get_resource_id, name='resource_id'),
    # general resource handler - FHIR is CaseSensitive!
    path('<resource>', views.get_resource, name='resource'),
    # path('CapabilityStatement', views.get_metadata,
    # name='capabilitystatement'),
    # path('Coverage', views.get_coverage,
    # name='coverage'),
    path('', views.index, name='index'),
]
