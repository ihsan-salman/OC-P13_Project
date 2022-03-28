'''!/usr/bin/python3
   -*- coding: Utf-8 -'''


from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    ''' comment form content widget config '''
    content = forms.CharField(widget=forms.Textarea(attrs={
         'rows': '4',
         'placeholder': 'Commentez ici...'
      }))

    class Meta:
        ''' class meta '''
        model = Comment
        fields = ['content']
