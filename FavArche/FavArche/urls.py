"""FavArche URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

from arche import views


HANDLER404 = 'registration.views.page_not_found'
HANDLER500 = 'registration.views.server_error'

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('arche.urls')),

    path('Inscription/', include('registration.urls')),

    path('Oeuvre/', include('work.urls')),

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