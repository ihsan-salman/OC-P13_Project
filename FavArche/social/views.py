'''!/usr/bin/python3
   -*- coding: Utf-8 -'''


import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError

from arche.models import Profile


def account(request, username):
	''' display other users personnal account page '''
	user = User.objects.get(username=username)
	user_image = Profile.objects.get(user=user)
	context = {'user_account': user, 'user_image': user_image}
	return render(request, 'social/account.html', context)