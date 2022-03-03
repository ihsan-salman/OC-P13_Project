'''!/usr/bin/python3
   -*- coding: Utf-8 -'''

"""FavArche URL Configuration
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

from arche import views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('arche.urls')),

    path('Inscription/', include('registration.urls')),

    path('Oeuvre/', include('work.urls')),

    path('Communaute/', include('social.urls')),

    url(r'^mon_compte/', views.personal_account, name='my_account'),
    url(r'^changer_mes_donnees/',
        views.edit_account,
        name='edit_account'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns