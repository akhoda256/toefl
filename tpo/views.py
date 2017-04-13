from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse

from django.http import HttpResponseRedirect
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def reading(request):
    return HttpResponse("Hello, world. You're at the polls index.")
	
@csrf_exempt
def index(request):
    return HttpResponse("index, world. You're at the polls index.")