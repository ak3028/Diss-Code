from django import forms

class ImageUploadForm(forms.Form):
    businessCardImage = forms.ImageField(label= "")