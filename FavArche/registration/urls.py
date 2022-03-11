'''!/usr/bin/python3
   -*- coding: Utf-8 -'''


from django.urls import path
from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('connexion/', views.CustomLoginView.as_view(), name='login'),
    path('creer_compte/', views.create_account, name='create_account'),
    path('deconnexion', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),

    path('change_password/', views.change_password, name='change_password'),

    path('reset_password/',
         auth_views.PasswordResetView.as_view(
            template_name='password-reset/password_reset.html'),
         name="reset_password"),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(
            template_name='password-reset/password_reset_sent.html'),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
            template_name='password-reset/password_reset_form.html'),
         name="password_reset_confirm"),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(
            template_name='password-reset/password_reset_done.html'),
         name="password_reset_complete"),

]