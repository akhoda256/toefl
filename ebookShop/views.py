from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt
from .models import Author,Book,Category,Publication


@csrf_exempt
def index(request):
    return render_to_response('tpo/index.html', {})


@csrf_exempt
def book(request):

    return render_to_response('ebookShop/book.html', {})

