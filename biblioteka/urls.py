from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.mainWeb, name='mainWeb'),
    path('category/<str:category>/', views.book_category, name='book_category'),
    path('author/<str:author>/', views.book_author, name='book_author'),
    path('publishingHouse/<str:publishingHouse>/', views.book_publishingHouse, name='book_publishingHouse'),
    path('/search/', views.book_search, name='book_search'),
    path('filters/', views.book_filtr, name='book_filtr'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('loginUser/', views.loginUser, name='loginUser'),
    path('registerUser/', views.registerUser, name='registerUser'),
    path('logout/', views.logout, name='logout'),

]