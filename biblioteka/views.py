from django.shortcuts import render
from .models import Book
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Max

import json

categories = Book.objects.values_list('category', flat=True).distinct()

z = json.loads('{}')


def categories_size(category, len):
    # appending the data
    z.update({category: len})


for category in categories:
    size = Book.objects.filter(category=category).count();
    name = category;
    categories_size(name, size)

# Create your views here.

books = Book.objects.all()

maxPrice = books.order_by('-price')[0].price


def mainWeb(request):
    return render(request, 'biblioteka/main.html', {'books': books, 'categories': z, 'maxPrice': maxPrice})


def book_category(request, category):
    books = Book.objects.filter(category=category)
    return render(request, 'biblioteka/main.html', {'books': books, 'categories': z, 'maxPrice': maxPrice})


def book_author(request, author):
    books = Book.objects.filter(author=author)
    return render(request, 'biblioteka/main.html', {'books': books, 'categories': z, 'maxPrice': maxPrice})


def book_publishingHouse(request, publishingHouse):
    books = Book.objects.filter(publishingHouse=publishingHouse)
    return render(request, 'biblioteka/main.html', {'books': books, 'categories': z, 'maxPrice': maxPrice})


def book_search(request):  # __icontains = lepsze wyszukiwanie
    search = request.GET.get('search').casefold()
    books = Book.objects.filter(
        Q(title__icontains=search) | Q(author__icontains=search) | Q(category__icontains=search) | Q(
            publishingHouse__icontains=search))
    return render(request, 'biblioteka/main.html', {'books': books, 'categories': z, 'maxPrice': maxPrice})


def book_filtr(request):  # new
    price1 = request.GET.get('price').casefold().replace('zł', '').split(' - ')
    author = request.GET.get('author').casefold()
    publishingHouse = request.GET.get('publishingHouse').casefold()
    if author and publishingHouse:
        books = Book.objects.filter(
            author=author, publishingHouse__icontains=publishingHouse, price__range=(price1[0], price1[1]))
    if author:  # author = 'TEXT'
        if not publishingHouse:  # publishingHouse = ''
            books = Book.objects.filter(author__icontains=author, price__range=(price1[0], price1[1]))
    if publishingHouse:  # publishingHouse = 'TEXT'
        if not author:  # author = ''
            books = Book.objects.filter(publishingHouse__icontains=publishingHouse, price__range=(price1[0], price1[1]))
    if not publishingHouse:
        if not author:
            books = Book.objects.filter(price__range=(price1[0], price1[1]))
    print(books)
    return render(request, 'biblioteka/main.html', {'books': books, 'categories': z, 'maxPrice': maxPrice})


def login(request):
    return render(request, 'biblioteka/login.html')


def register(request):
    return render(request, 'biblioteka/register.html')


from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect


def loginUser(request):
    username = request.POST.get('login')
    password = request.POST.get('password')
    print(username)
    print(password)
    user = authenticate(request, username=username, password=password)
    if user is not None:
        django_login(request, user)
        # Redirect to a success page.
        return HttpResponseRedirect("/")
    else:
        return render(request, 'biblioteka/login.html', {'valid': 'Niepoprawne dane logowania!'})
        # Return an 'invalid login' error message.


def registerUser(request):
    username = request.POST.get('login')
    password = request.POST.get('password')
    password2 = request.POST.get('password2')
    # simple check data
    if username and password and password2:
        if password == password2:
            if username != password2:
                user = User.objects.create_user(username, '', password2)
                django_login(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect("/")
            else:
                return render(request, 'biblioteka/register.html',
                              {'valid': 'Nie ustawiaj takiego samego hasla jak login!'})
        else:
            return render(request, 'biblioteka/register.html', {'valid': 'Hasła nie są takie same!'})
    else:
        return render(request, 'biblioteka/register.html', {'valid': 'Pole są puste!'})


@login_required
def logout(request):
    django_logout(request)
    return HttpResponseRedirect('/')
