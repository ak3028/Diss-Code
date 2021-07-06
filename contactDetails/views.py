from django.shortcuts import render
from pathlib import Path
from PIL import Image
import pytesseract

# Build paths inside the project like this: BASE_DIR / 'subdir'.
base_path = Path(__file__).resolve().parent.parent

# Create your views here.
def index(request):
    if request.method == "GET":
        base_path = str(Path(__file__).resolve().parent.parent)
        imageUrl = request.GET.get('imageUrl')
        imagePath = base_path + '/uploadedFiles/' + imageUrl
        cardInfoString = runOcrOnCard(imagePath)
        return render(request, "contactDetails/contactDetailForm.html", {"cardInfo": cardInfoString})

    elif request.method == "POST":
        return render(request, "contactDetails/contactDetailForm.html")
    

def runOcrOnCard(imageUrl):
    cardInfo = pytesseract.image_to_string(Image.open(imageUrl))
    cardInfo = cardInfo.strip()
    return cardInfo
    