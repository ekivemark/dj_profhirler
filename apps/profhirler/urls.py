"""
profhirler views

"""
from django.urls import path

from . import views

urlpatterns = [
    path('Metadata', views.get_metadata, name='metadata'),
    path('CapabilityStatement', views.get_metadata, name='capabilitystatement'),
    path('', views.index, name='index'),
]
