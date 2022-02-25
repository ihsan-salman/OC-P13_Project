'''!/usr/bin/python3
   -*- coding: Utf-8 -'''


from django import forms

from .models import Comment

class CommentForm(forms.ModelForm):
   content = forms.CharField(widget=forms.Textarea(attrs={
         'rows': '4',
         'placeholder':'Commentez ici...'
      }))

   class Meta:
      '''  '''
      model = Comment
      fields = ['content']
