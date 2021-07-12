from contactDetails.models import Contact
from django.contrib import admin

from .models import BusinessCard

admin.site.register(BusinessCard)
admin.site.register(Contact)

# Register your models here.
