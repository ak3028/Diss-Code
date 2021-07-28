from businessContacts.models import BusinessContact
from django.contrib import admin

from .models import BusinessCard

admin.site.register(BusinessCard)
admin.site.register(BusinessContact)

# Register your models here.
