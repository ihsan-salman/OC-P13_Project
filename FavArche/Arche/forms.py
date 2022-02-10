'''!/usr/bin/python3
   -*- coding: Utf-8 -'''

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend, UserModel
from django.contrib.auth.forms import AuthenticationForm, UsernameField


class RegisterForm(UserCreationForm):
    '''Register form class'''
    email = forms.EmailField()

    class Meta:
        '''Making line between the form and User model'''
        model = User
        fields = ["username", "email", "first_name", "last_name","password1", "password2"]


class CustomAuthenticationForm(AuthenticationForm):
    '''change username label in login form to email label'''
    username = UsernameField(
        label='Identfiant',
        widget=forms.TextInput(attrs={'autofocus': True})
    )


class EditProfileForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]


class ContactForm(forms.Form):
    email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)