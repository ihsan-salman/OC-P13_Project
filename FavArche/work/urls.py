'''!/usr/bin/python3
   -*- coding: Utf-8 -'''


from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('personnel/', views.personal_works, name='personal_works'),
    path('ajout/', views.add_works, name='add_works'),
    path('favoris/', views.favorite_works, name='fav_works'),
    path('categorie/', views.add_category, name='add_category'),

]