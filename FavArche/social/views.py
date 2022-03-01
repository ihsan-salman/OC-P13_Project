'''!/usr/bin/python3
   -*- coding: Utf-8 -'''


import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError

from arche.models import Profile
from work.models import Works
from .models import Comment, Like


def account(request, username):
    ''' display other users personnal account page '''
    user = User.objects.get(username=username)
    user_image = Profile.objects.get(user=user)
    context = {'user_account': user, 'user_image': user_image}
    return render(request, 'social/account.html', context)


def delete_comment(request):
    ''' delete comment on post method '''
    if request.method == 'POST':
        comment_id = request.POST.get("comment_id")
        comment = Comment.objects.get(id=comment_id)
        comment.delete()
        return HttpResponse('OK')


def like(request):
    '''  '''
    user = User.objects.get(username=request.user.username)
    if request.method == 'POST':
        work_id = request.POST.get("work_id")
        work_obj = Works.objects.get(id=work_id)

        if user in work_obj.liked.all():
            work_obj.liked.remove(user)
        else:
            work_obj.liked.add(user)

        like, created = Like.objects.get_or_create(user=user, work_id=work_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        like.save()

        return HttpResponse('OK')