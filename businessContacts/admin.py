from businessContacts.models import BusinessContact
from django.contrib import admin

class BusinessContactAdmin(admin.ModelAdmin):
    list_filter = ("contactName","contactOrganization", "contactOrganization", "contactPhoneNumber","contactCardInfo",)
    list_display = ("contactName","contactOrganization", "contactOrganization", "contactPhoneNumber","contactCardInfo",)

admin.site.register(BusinessContact,BusinessContactAdmin)


  

