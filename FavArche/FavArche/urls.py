'''!/usr/bin/python3
   -*- coding: Utf-8 -'''

"""FavArche URL Configuration
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf.urls import handler404
from django.conf.urls import include, url
from django.views.static import serve
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

from main import views


handler404 = 'registration.views.page_not_found'
HANDLER500 = 'registration.views.server_error'

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('main.urls')),

    path('Inscription/', include('registration.urls')),

    path('Oeuvre/', include('work.urls')),

    path('Communaute/', include('social.urls')),

    url(r'^mon_compte/', views.personal_account, name='my_account'),
    url(r'^changer_mes_donnees/',
        views.edit_account,
        name='edit_account'),
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns