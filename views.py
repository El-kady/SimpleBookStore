from django.shortcuts import render
from django.views.generic import ListView

from .models import Book

class Index(ListView):
    model = Book
    template_name = 'SimpleBookStore/index.html'
