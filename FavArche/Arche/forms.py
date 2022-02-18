'''!/usr/bin/python3
   -*- coding: Utf-8 -'''


from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User


class EditProfileForm(UserChangeForm):
    ''' custom edit profile form '''
    password = None

    class Meta:
        ''' define model and input fields form '''
        model = User
        fields = ["username", "email", "first_name", "last_name"]
