from django.db.models.fields import DateField
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse    
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

    elif request.method == "DELETE":
        # businessCardToBeDeleted = BusinessCard.objects.get(id=request.imageId)
        # businessCardToBeDeleted.delete()
        print('alok1')
        # body_unicode = request.body.decode('utf-8')
        
        # content = body_unicode['imageId']
        # json_params = json.loads(request.body)
        print(request.GET.get('imageId'))
        print('alok1')
        BusinessCard.objects.get(pk=25).delete()
        return render(request, "uploadBusinessCard/businessCards.html")




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

