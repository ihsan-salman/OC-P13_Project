'''!/usr/bin/python3
   -*- coding: Utf-8 -'''

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UsernameField


class RegisterForm(UserCreationForm):
    '''Register form class'''
    email = forms.EmailField()
    first_name = forms.CharField(label='Prénom', required=True)
    last_name = forms.CharField(label='Nom de famille', required=True)

    class Meta:
        '''Making line between the form and User model'''
        model = User
        fields = ["username", "email", "first_name", "last_name",
                  "password1", "password2"]


class CustomAuthenticationForm(AuthenticationForm):
    '''change username label in login form to email label'''
    username = UsernameField(
        label='Identfiant',
        widget=forms.TextInput(attrs={'autofocus': True})
    )


class EditProfileForm(UserChangeForm):
    ''' Edit profile form class '''
    password = None

    class Meta:
        ''' meta class '''
        model = User
        fields = ["username", "email", "first_name", "last_name"]
