'''!/usr/bin/python3
   -*- coding: Utf-8 -'''


from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('contact/', views.contact, name='contact'),
    path('a_propos/', views.about_us, name='about_us'),
    path('fonctionnalité/', views.functionality, name='functionality'),
    path('categories/', views.category, name='category'),
]
