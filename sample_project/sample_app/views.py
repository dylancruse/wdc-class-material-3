from datetime import datetime

from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages

from .models import Author, Book


def index(request):
    sort_method = request.GET.get('sort', 'asc')
    books = Book.objects.all()
    if sort_method == 'asc':
        books = books.order_by('popularity')
    elif sort_method == 'desc':
        books = books.order_by('-popularity')
    query = request.GET.get('query')
    if query:
        books = books.filter(title__icontains=query)
    return render(request, 'index.html', {
        'books': books,
        'authors': Author.objects.all(),
        'sort_method': sort_method
    })


def create_book(request):
    messages.success(request, 'Book has been created!')
    book_data = {
        'title': request.POST['title'],
        'author': request.POST['author'],
        'isbn': request.POST['isbn'],
        'popularity': request.POST['popularity'],
    }
    
    author = get_object_or_404(Author, id=request.POST['author'])
    book = Book.objects.create(
        author=author,
        title=request.POST['title'],
        isbn=request.POST['isbn'],
        popularity=request.POST['popularity']
        )
    
    return render(request, 'create_book.html', {
        'data': book_data,
        'book_created': book
    })


def authors(request):
    authors = Author.objects.all()
    return render(request, 'authors.html', {
        'authors': authors
    })


def author(request, author_id):
    try:
        author = Author.objects.get(id=author_id)
    except Author.DoesNotExist:
        return HttpResponseNotFound()

    return render(request, 'author.html', {
        'author': author
    })
