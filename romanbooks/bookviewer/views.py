from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.db.models import Count

from .models import Book

def categories(request):
    book_categories = Book.objects.values('category').order_by('category').annotate(count=Count('category'))
    template = loader.get_template('bookviewer/categories.html')
    context = {
        'categories': book_categories,
    }
    return HttpResponse(template.render(context, request))

def book_category(request, cat):
    books_in_category = Book.objects.filter(category = cat).order_by('title')
    template = loader.get_template("bookviewer/book_category.html")
    context = {
        'category': cat,
        'books': books_in_category
    }
    return HttpResponse(template.render(context, request))

def detail(request, title):
    return HttpResponse("You're looking at {}.".format(title))