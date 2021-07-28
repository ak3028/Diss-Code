from django.db.models.fields import DateField
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views import View
from django.http import HttpResponse
from django.views.generic.base import RedirectView    
from django.http import QueryDict
from django.views.generic.edit import CreateView
from uploadBusinessCard.models import BusinessCard


# class CreateImageUploadView(CreateView):
#     template_name = "uploadBusinessCard/imageUpload.html"
#     model = BusinessCard
#     fields = ['image']
#     success_url = "/uploadBusinessCard"


def businessCards(request):
    if request.method == "GET":
        businessCards = BusinessCard.objects.order_by('isProcessed').all()
        return render(request, "processBusinessCards/businessCards.html", {"cardList": businessCards})


    elif request.method == "POST":
        # get the id of the business card that needs to be deleted from the database
        businessCardId= request.POST.get('imageId') 
        BusinessCard.objects.get(pk=businessCardId).delete()
        return HttpResponseRedirect("/processBusinessCards")


