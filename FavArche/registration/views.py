'''!/usr/bin/python3
   -*- coding: Utf-8 -'''


import os
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm

from .forms import RegisterForm, CustomAuthenticationForm, EditProfileForm
from arche.models import Profile


def create_account(request):
    '''return the template to create an user account
       and add in the database all related information'''
    context = {}
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            name = request.POST.get('username')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            password = make_password(request.POST.get('password1'))
            user = User.objects.filter(username=name)
            if not user.exists():
                # If a contact is not registered, create a new one.
                user = User.objects.create(
                    username=name,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=password
                )
                user.save()
                print(user)
                profile_user = Profile.objects.create(
                    user=user.id)
                profile_user.save()
                print(profile_user)
            else:
                user = user.first()

            return redirect('/connexion/')
        else:
            # Form data doesn't match the expected format.
            # Add errors to the template.
            context['errors'] = form.errors.items()
    else:
        form = RegisterForm()
    return render(request, 'registration/create_account.html', {'form': form})


class CustomLoginView(LoginView):
    ''' Standart login form and class as view '''
    authentication_form = CustomAuthenticationForm


@login_required(login_url='/login/')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse('accounts:view_profile'))
        else:
            return redirect(reverse('accounts:change_password'))
    else:
        form = PasswordChangeForm(user=request.user)

        context = {'form': form}
    return render(request, 'registration/change_password.html', context)


def page_not_found(request, exception):
    '''return the 404 error page'''
    return render(request, 'error_page/404.html', status=404)


def server_error(request):
    '''return the 500 error page'''
    return render(request, 'error_page/500.html', status=500)
