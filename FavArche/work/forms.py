'''!/usr/bin/python3
   -*- coding: Utf-8 -'''

from django import forms

from .models import Works, Category


class ContactForm(forms.Form):
    ''' Contact Form fields '''
    email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)


class CategoryForm(forms.ModelForm):
    ''' Category form with cdkeditor Text field '''
    class Meta:
        model = Category
        fields = ['name', 'description']


class EditCategoryForm(forms.ModelForm):
    ''' Category form with cdkeditor Text field '''
    class Meta:
        model = Category
        fields = ['description']


class WorksDescriptionForm(forms.ModelForm):
    ''' Works description form with cdkeditor text field '''
    class Meta:
        model = Works
        fields = ['description']
