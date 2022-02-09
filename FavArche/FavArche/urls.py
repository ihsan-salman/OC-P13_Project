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
from django.conf.urls.static import  static
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

from Arche import views


HANDLER404 = 'mes_aliments.views.page_not_found'
HANDLER500 = 'mes_aliments.views.server_error'

urlpatterns = [
    url(r'^$', views.index, name = 'home'),
    path('admin/', admin.site.urls),

    url(r'^create_account/', views.create_account, name='create_account'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), {'next_page':
        settings.LOGOUT_REDIRECT_URL}, name='logout'),

    path('reset_password/',
         auth_views.PasswordResetView.as_view(
            template_name='registration/password-reset/password_reset.html'),
         name="reset_password"),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password-reset/password_reset_sent.html'),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password-reset/password_reset_form.html'),
         name="password_reset_confirm"),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password-reset/password_reset_done.html'),
         name="password_reset_complete"),

    url(r'^my_account/', views.personal_account, name='my_account'),
    url(r'^edit_account_information/',
        views.edit_account,
        name='edit_account'),
    url(r'^change_password/', views.change_password, name='change_password'),

    url(r'^my_works/', views.personal_works, name='personal_works'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns