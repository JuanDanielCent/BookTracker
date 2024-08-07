from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import Author, Book
from .forms import AuthorForm, BookForm
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password2'])
                user.save()
                login(request, user)
                return redirect('index')
            except:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'User already created'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Passwords do not match'
        })

    return render(request, 'signup.html', {
        'form': UserCreationForm
    })

def signin(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'login.html', {
                'form': AuthenticationForm,
                'error': 'Username or password incorrect'
            })
        else:
            login(request, user)
            return redirect('index')
    return render(request, 'login.html', {
        'form': AuthenticationForm
    })

@login_required
def signout(request):
    logout(request)
    return redirect('index')

@login_required
def author(request):
    author = Author.objects.filter(user=request.user)
    return render(request, 'author.html', {
        'author': author
    })

@login_required
def book(request):
    book = Book.objects.filter(user=request.user)
    return render(request, 'book.html', {
        'book': book
    })

@login_required
def add_author(request):
    form = AuthorForm(request.POST or None)
    if form.is_valid():
        new_author = form.save(commit=False)
        new_author.user = request.user
        new_author.save()
        return redirect('author')
    return render(request, 'add_author.html', {
        'form': AuthorForm()
    })

@login_required
def add_book(request):
    if request.method == 'POST':
        book_form = BookForm(request.POST, user=request.user)
        if book_form.is_valid():
            author_existing = book_form.cleaned_data['author_existing']
            author_new = book_form.cleaned_data['author_new']

            if author_new:
                author = Author.objects.create(name=author_new, user=request.user)
            else:
                author = author_existing

            book = book_form.save(commit=False)
            book.author = author
            book.user = request.user
            book.save()
            return redirect('book')
    book_form = BookForm(user=request.user)
    return render(request, 'add_book.html', {
        'form': book_form
    })

@login_required
def update(request, pk):
    book = get_object_or_404(Book, pk=pk, user=request.user)
    form = BookForm(request.POST or None, instance=book, user=request.user)
    if form.is_valid():
        author_existing = form.cleaned_data['author_existing']
        author_new = form.cleaned_data['author_new']

        if author_new:
            author = Author.objects.create(name=author_new, user=request.user)
        else:
            author = author_existing

        book = form.save(commit=False)
        book.author = author
        book.user = request.user
        book.save()
        return redirect('book')
    return render(request, 'update.html', {
        'book': book,
        'form': form
    })

@login_required
def books_of_author(request, pk):
    author = get_object_or_404(Author, pk=pk)
    books = Book.objects.filter(author_id=pk)
    return render(request, 'books_of_author.html', {
        'author': author,
        'books': books
    })

@login_required
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return redirect('book')

@login_required
def done_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.done = True
    book.save()
    return redirect('book')

@login_required
def update_author(request, pk):
    author = get_object_or_404(Author, pk=pk)
    form = AuthorForm(request.POST or None, instance=author)
    if form.is_valid():
        author_form = form.save(commit=False)
        author_form.user = request.user
        author_form.save()
        return redirect('author')
    return render(request, 'update_author.html', {
        'form': form
    })

@login_required
def delete_author(request, pk):
    author = get_object_or_404(Author, pk=pk)
    author.delete()
    return redirect('author')