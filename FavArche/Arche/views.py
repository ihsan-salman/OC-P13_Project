'''!/usr/bin/python3
   -*- coding: Utf-8 -'''


import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError

from .forms import EditProfileForm


def index(request):
    ''' Return index page result '''
    return render(request, 'favarche/index.html')


def contact(request):
    ''' Return contact page result '''
    if request.method == 'POST':
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        email_message = request.POST.get("message")
        print(email, subject, email_message)
        try:
            send_mail(subject,
                      email_message,
                      email,
                      [os.environ['EMAIL_HOST_USER']])
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return redirect('/contact/')
    return render(request, 'favarche/informative/contact.html')


def about_us(request):
    ''' Return about page result '''
    return render(request, 'favarche/informative/about.html')


def functionality(request):
    ''' Return functionality page result '''
    return render(request, 'favarche/informative/functionality.html')


@login_required(login_url='/login/')
def personal_account(request):
    ''' return the template of user's personal informations '''
    return render(request, 'favarche/account/my_account.html')


@login_required(login_url='/login/')
def edit_account(request):
    '''return the template to change user's personal informations '''
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/my_account/')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request,
                  'favarche/account/edit_account.html',
                  {'form': form})
