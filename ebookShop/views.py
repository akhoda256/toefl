from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt
from .models import Author, Book, Category, Publication


@csrf_exempt
def index(request):
    cats = Category.objects.all()

    return render_to_response('ebookShop/home.html', {})


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
