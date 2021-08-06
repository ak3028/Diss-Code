from django.db.models.fields import DateField
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views import View
from django.http import HttpResponse
from django.views.generic.base import RedirectView    
from .forms import ImageUploadForm
from .models import BusinessCard
import datetime
import json
from django.http import QueryDict
from django.views.generic.edit import CreateView
from uploadBusinessCard import models



class CreateImageUploadView(View):
    def get(self, request):
        form = ImageUploadForm()
        return render(request, "uploadBusinessCard/imageUpload.html", { 
            "form" : form })
    
    def post(self, request):
        submittedForm = ImageUploadForm(request.POST, request.FILES)
        if submittedForm.is_valid():
            businessCard = BusinessCard(image=request.FILES["businessCardImage"], submittedBy = "admin", 
                                               submittedDate = datetime.datetime.now(), isProcessed = "N")
            businessCard.save()

        return render(request, "uploadBusinessCard/imageUpload.html", {
            "form": submittedForm
        })

