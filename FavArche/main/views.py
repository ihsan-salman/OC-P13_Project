'''!/usr/bin/python3
   -*- coding: Utf-8 -'''


import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError

from .forms import EditProfileForm
from work.models import Works, Category
from .models import Profile
from social.models import Comment
from social.forms import CommentForm


def index(request):
    ''' Return index page result '''
    users = User.objects.all()
    user_image_list1 = []
    for user in users:
        if user.username != request.user.username:
            image = Profile.objects.get(user=user)
            user_image_list1.append(image)
    works = Works.objects.filter(time__year=2022)
    user_image_list2 = []
    comment_list = []
    for work in works:
        user = User.objects.get(username=work.user)
        image = Profile.objects.get(user=user)
        comment = Comment.objects.filter(work=work.id)
        user_image_list2.append(image)
        comment_list.append(comment)
    if request.method == 'POST':
        work_id = request.POST.get('work_id')
        comment = request.POST.get('comment')
        user_work = Works.objects.get(id=work_id)
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user.username)
        elif not User.objects.filter(username='anonymous').exists():
            user = User.objects.create(
                username='anonymous',
                email='ano@nymous.com',
                first_name='ano',
                last_name='nymous',
                password=make_password(os.environ['ANONYMOUS_PASSWORD']))
        if comment != '':
            user_comment = Comment.objects.create(
                content=comment,
                user=user,
                work=user_work)
    if request.is_ajax():
        return HttpResponse("OK")
    context = {'works': works,
               'user_image': user_image_list2,
               'users': users,
               'social_user_img': user_image_list1,
               'comment_list': comment_list}
    return render(request, 'favarche/index.html', context)


def contact(request):
    ''' Return contact page result '''
    if request.method == 'POST':
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        email_message = request.POST.get("message")
        if email != '' or subject != '' or email_message != '':
            try:
                send_mail(subject,
                          email_message,
                          email,
                          [os.environ['EMAIL_HOST_USER']])
                return redirect('/')
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
        else:
             return render(request, 'error_page/404.html', status=404)
    return render(request, 'favarche/informative/contact.html')


def about_us(request):
    ''' Return about page result '''
    return render(request, 'favarche/informative/about.html')


def functionality(request):
    ''' Return functionality page result '''
    return render(request, 'favarche/informative/functionality.html')


def category(request):
    ''' Return category page result '''
    number_list = []
    for i in range(Category.objects.count()):
        number_list.append(i + 1)
    context = {'categories': Category.objects.all(),
               'number_list': number_list}
    return render(request, 'favarche/informative/category.html', context)


@login_required(login_url='/login/')
def personal_account(request):
    ''' return the template of user's personal informations '''
    user = User.objects.get(username=request.user.username)
    user_profile_img = Profile.objects.get(user=user)
    if request.method == 'POST':
        user_profile_img.image = request.FILES['user_img']
        user_profile_img.save()
    context = {'img': user_profile_img}
    return render(request, 'favarche/account/my_account.html', context)


@login_required(login_url='/login/')
def edit_account(request):
    '''return the template to change user's personal informations '''
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/mon_compte/')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request,
                  'favarche/account/edit_account.html',
                  {'form': form})