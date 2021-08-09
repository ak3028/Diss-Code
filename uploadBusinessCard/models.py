from django.db import models

class BusinessCard(models.Model):
    # imageLocation = models.CharField(max_length=100)
    image = models.ImageField(upload_to="businessCardImages", null=False)
    submittedBy = models.CharField(max_length=200)
    submittedDate = models.DateField(null=False)
    isProcessed = models.CharField(max_length=1, null=False)
    


# this function is used to overreide the string object which is used to represent
# an object in the database. Its used when we query the database from the python shell
    def __str__(self):
        return f"{self.id}, {self.image}"

