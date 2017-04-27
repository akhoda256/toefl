from django import forms

class UploadFileForm(forms.Form):
    user = forms.CharField(max_length=200)
    respFile = forms.FileField()