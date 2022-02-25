'''!/usr/bin/python3
   -*- coding: Utf-8 -'''


from django.urls import path
from django.conf import settings
from django.conf.urls import url
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
   path('compte/<str:username>', views.account, name='other_accounts'),
]