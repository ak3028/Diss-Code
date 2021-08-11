from django.contrib import admin
from .models import BusinessCard

class BusinessCardAdmin(admin.ModelAdmin):
    list_filter = ("image","submittedBy", "submittedDate", "isProcessed",)
    list_display = ("image","submittedBy", "submittedDate", "isProcessed",)

admin.site.register(BusinessCard,BusinessCardAdmin)


# Register your models here.
