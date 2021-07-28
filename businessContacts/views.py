from businessContacts.models import BusinessContact
from django.shortcuts import render
from pathlib import Path
from PIL import Image
import pytesseract
from django.contrib import messages
from .models import BusinessContact
from .imageProcessing import imagePreProcessor
from .imageProcessing import textProcessor
# Build paths inside the project like this: BASE_DIR / 'subdir'.
base_path = Path(__file__).resolve().parent.parent

# Create your views here.
def index(request):
    if  request.method == "GET":
        base_path = str(Path(__file__).resolve().parent.parent)
        imageUrl = request.GET.get('imageUrl')
        imagePath = base_path + '/uploadedFiles/' + imageUrl
        cardInfoString, name, org, email, mobile, remainingText = runOcrOnCard(imagePath)
        return render(request, "businessContacts/contactDetailForm.html", {"cardInfo": cardInfoString, 
                                                                         "contactName": name,
                                                                         "mobileNo": mobile,
                                                                         "email": email,
                                                                         "organization" : org,
                                                                         "remainingText": remainingText
                                                                         })

    elif request.method == "POST":
        contactName = request.POST['contactName']
        organization = request.POST['organization']
        email = request.POST['email']
        phone = request.POST['phone']
        cardText = request.POST['inputCardText']
        #populate the contact details in the model and save the contact in the database
        #display the success message after saving the contact
        contact = BusinessContact(contactName=contactName, contactOrganization=organization, contactEmail=email, 
                        contactPhoneNumber=phone,contactCardInfo=cardText)

        contact.save()
        messages.success(request,'Contact has been successfully saved in the database.')
        return render(request, "businessContacts/contactDetailForm.html")
    
def businessContacts(request):
     contacts = BusinessContact.objects.all() 
     return render(request, "businessContacts/businessContacts.html",{"contacts": contacts})


def runOcrOnCard(imageUrl):
    cardInfo = imagePreProcessor.getAllTextFromCard(imageUrl)
    cardText, name, org, email, phone, remainingText = textProcessor.processCardText(cardInfo)
    return (cardText, name, org, email, phone, remainingText)



    