from django.urls import path
from django.views.generic.base import View
from . import views

urlpatterns = [   
      path("contactDetail", views.index),
      path("contacts", views.contacts) 
    
]
