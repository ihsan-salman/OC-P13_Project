'''!/usr/bin/python3
   -*- coding: Utf-8 -'''


from django.urls import path
from django.conf import settings
from django.conf.urls import url
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('personnel/', views.personal_works, name='personal_works'),
    path('ajout_oeuvre/', views.add_works, name='add_works'),
    path('edition_oeuvre/<str:work_name>/',
         views.edit_works,
         name='edit_work'),
    path('favoris/', views.favorite_works, name='fav_works'),
    path('ajout_categorie/', views.add_category, name='add_category'),
    path('edition_categorie/<str:category_name>/',
         views.edit_category,
         name='edit_category'),
    path('detail/<str:work_name>/', views.work_details, name='work_details'),
    path('recherche_par_catégorie/<str:category_name>/',
         views.search_by_category,
         name='search_by_category'),
    path('recherche_par_oeuvre/', views.search_by_work, name='search_by_work' ),
    path('', views.get_wiki, name='wiki_data'),

]