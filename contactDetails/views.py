from contactDetails.models import Contact
from django.shortcuts import render
from pathlib import Path
from PIL import Image
import pytesseract
from django.contrib import messages
from .models import Contact
from .imageProcessing import imagePreProcessor

# Build paths inside the project like this: BASE_DIR / 'subdir'.
base_path = Path(__file__).resolve().parent.parent

# Create your views here.
def index(request):
    if  request.method == "GET":
        base_path = str(Path(__file__).resolve().parent.parent)
        imageUrl = request.GET.get('imageUrl')
        imagePath = base_path + '/uploadedFiles/' + imageUrl
        cardInfoString = runOcrOnCard(imagePath)
        return render(request, "contactDetails/contactDetailForm.html", {"cardInfo": cardInfoString})

    elif request.method == "POST":
        contactName = request.POST['contactName']
        organization = request.POST['organization']
        email = request.POST['email']
        phone = request.POST['phone']
        cardText = request.POST['inputCardText']
        #populate the contact details in the model and save the contact in the database
        #display the success message after saving the contact
        contact = Contact(contactName=contactName, contactOrganization=organization, contactEmail=email, 
                        contactPhoneNumber=phone,contactCardInfo=cardText)

        contact.save()
        messages.success(request,'Contact has been successfully saved in the database.')
        return render(request, "contactDetails/contactDetailForm.html")
    
def contacts(request):
     contacts = Contact.objects.all() 
     return render(request, "contactDetails/contacts.html",{"contacts": contacts})


def runOcrOnCard(imageUrl):

    # cardInfo = pytesseract.image_to_string(Image.open(imageUrl))
    cardInfo = imagePreProcessor.getAllTextFromCard(imageUrl)
    cardInfo = cardInfo.strip()
    return cardInfo



    