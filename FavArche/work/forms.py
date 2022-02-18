'''!/usr/bin/python3
   -*- coding: Utf-8 -'''

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend, UserModel
from django.contrib.auth.forms import AuthenticationForm, UsernameField

from .models import Works, Category


class ContactForm(forms.Form):
    email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)


class ImageForm(forms.ModelForm):
    """ Form for the image field in Works model """
    class Meta:
        model = Works
        fields = ["image"]