from django import forms
from .models import SpeakingResponse

class SpeakingResponseForm(forms.Form):
    user = forms.CharField(max_length=200)
    respFile = forms.FileField()
    tpoNo = forms.IntegerField()
    questionNo = forms.IntegerField()



