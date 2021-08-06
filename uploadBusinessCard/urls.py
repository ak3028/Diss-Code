from django.urls import path
from django.views.generic.base import View
from . import views

urlpatterns = [
      path("", views.CreateImageUploadView.as_view()) 
]
