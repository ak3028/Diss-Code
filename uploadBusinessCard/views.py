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


# class CreateImageUploadView(CreateView):
#     template_name = "uploadBusinessCard/imageUpload.html"
#     model = BusinessCard
#     fields = ['image']
#     success_url = "/uploadBusinessCard"


def scannedCards(request):
    if request.method == "GET":
        businessCards = BusinessCard.objects.order_by('isProcessed').all()
        # Author.objects.order_by('-score')
        return render(request, "uploadBusinessCard/businessCards.html", {"cardList": businessCards})
    
    # elif request.method == "POST":

    #     return render(request, "uploadBusinessCard/businessCards.html")

    elif request.method == "POST":
        # get the id of the business card that needs to be deleted from the database
        businessCardId= request.POST.get('imageId') 
        BusinessCard.objects.get(pk=businessCardId).delete()
        return HttpResponseRedirect("/uploadBusinessCard/scannedCards")




# Create your views here.
# def index(request):
#     if request.method == "GET":
#      return render(request, "uploadBusinessCard/imageUpload.html")
    
#     elif request.method == "POST":
#         return render(request, "uploadBusinessCard/imageUpload.html")

# The below code has been replaced by a simple CreateView defined above which doesnt need declaration of get and post method
# with this change we can get rid of the forms class and its not needed anymore

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

