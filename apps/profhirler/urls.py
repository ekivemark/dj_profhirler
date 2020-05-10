"""
profhirler views

"""
from django.urls import path

from . import views

urlpatterns = [
    path('UpdatePatient', views.change_patient, name="change_patient"),
    path('Metadata', views.get_metadata, name='metadata'),
    path('<resource>/<_id>', views.get_resource_id, name='resource_id'),
    # general resource handler - FHIR is CaseSensitive!
    path('<resource>', views.get_resource, name='resource'),
#    path('CapabilityStatement', views.get_metadata, name='capabilitystatement'),
#    path('Coverage', views.get_coverage, name='coverage'),
    path('', views.index, name='index'),
]
