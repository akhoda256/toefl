from django.contrib.auth.models import User
from django.middleware import csrf
from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt
from .models import Author,Book,Category,Publication

from toefl import settings
from .models import Author, Book, Category, Publication, BasketItem
from django.http import JsonResponse

@csrf_exempt
def index(request):
    cats = Category.objects.all()

    return render_to_response('ebookShop/home.html', {})
 #return render_to_response('ebookShop/index.html', {})


@csrf_exempt
def book(request):
    myBook = Book.objects.first()
    suggestionList = Book.objects.all()
    return render_to_response('ebookShop/book.html',
                              {'book': myBook, 'suggestions': suggestionList})


@csrf_exempt
def category(request):
    cat = Category.objects.first()
    books = Book.objects.filter(category=cat)
    return render_to_response('ebookShop/cat.html', {'books': books, 'cat': cat})

@csrf_exempt
def addBasket(request):
    resp = {'status' : ''}
    if request.method == 'GET':
        resp['status'] = 'failed'
    elif request.method == 'POST':
        userId = request.POST.get('userId', None)
        bookId = request.POST.get('bookId', None)
        csrfToken = request.META.get('CSRF_COOKIE', None)
        obj = BasketItem.objects.get(user_id=userId, book_id=bookId)
        if obj == None:
            basketItem = BasketItem(user_id=userId, book_id = bookId, csrfToken=csrfToken)
            basketItem.save()
            resp['status'] = 'success'
        else:
            resp['status'] = 'error'
    return JsonResponse(resp)
