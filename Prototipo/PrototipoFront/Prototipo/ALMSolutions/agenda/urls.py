from django.conf.urls import url
from django.urls import path
from agenda.views import home, agenda, api

urlpatterns = [
    path('', home),
    path('api/', api),
    path('agenda/', agenda),
]
