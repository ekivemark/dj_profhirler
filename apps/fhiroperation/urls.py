"""
fhiroperation
"""
from django.urls import path

from . import views


urlpatterns = [
    path('$member-match', views.get_membermatch, name='membermatch'),
    path('', views.index, name='index'),
]
