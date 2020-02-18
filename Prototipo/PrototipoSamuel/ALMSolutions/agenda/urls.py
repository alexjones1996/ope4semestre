from django.conf.urls import url
from django.urls import path
from agenda import views 
urlpatterns = [
    path('', views.index),
    path('eventos', views.home),
    path('agenda/', views.agenda),
]
