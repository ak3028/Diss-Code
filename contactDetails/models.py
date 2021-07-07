from django.db import models
from uploadBusinessCard.models import BusinessCard, models

# Create your models here.
class Contact(models.Model):
    contactName = models.CharField(max_length=300)
    contactOrganization = models.CharField(max_length=200)
    contactEmail = models.EmailField(max_length=100)
    contactPhoneNumber = models.CharField(max_length=20)
    contactCardInfo = models.CharField(max_length=1000)
    models.ForeignKey(BusinessCard, on_delete=models.CASCADE)