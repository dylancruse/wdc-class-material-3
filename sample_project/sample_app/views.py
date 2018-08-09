from datetime import datetime

from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages

from .models import Author, Book


def index(request):
    errors = {}
    form_values = {
        'title': '',
        'isbn': ''
    }
    if request.method == 'POST':
        title = request.POST.get('title')
        popularity = request.POST.get('popularity')
        isbn = request.POST.get('isbn')
        if not isbn:
            errors['isbn'] = 'ISBN cannot be blank'
        else:
            form_values['isbn'] = isbn
        if not title:
            errors['title'] = 'Title cannot be blank'
        else:
            form_values['title'] = title
        try:
            popularity = float(popularity)
        except ValueError:
            errors['popularity'] = 'Invalid Value'
        #still need to create the book in the database
        
    # GET:
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
        'errors': errors,
        'form_values': form_values,
        'authors': Author.objects.all(),
        'sort_method': sort_method
    })


def create_book(request):
    title = request.POST.get('title')
    if not title:
        messages.error(request, 'Missing field')
        return redirect('/?errors=1&error_title=1')
    
    author = get_object_or_404(Author, id=request.POST['author'])
    book = Book.objects.create(
        author=author,
        title=request.POST['title'],
        isbn=request.POST['isbn'],
        popularity=request.POST['popularity']
        )
    book_data = {
        'title': request.POST['title'],
        'author': request.POST['author'],
        'isbn': request.POST['isbn'],
        'popularity': request.POST['popularity'],
    }
    messages.success(request, 'Book has been created!')
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
