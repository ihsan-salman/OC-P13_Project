'''!/usr/bin/python3
   -*- coding: Utf-8 -'''


from django.urls import path
from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('contact/', views.contact, name = 'contact'),
    path('a_propos/', views.about_us, name = 'about_us'),
    path('fonctionnalité/', views.functionality, name = 'functionality'),

]