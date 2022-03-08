'''!/usr/bin/python3
   -*- coding: Utf-8 -'''


import os
import json
from django.core import serializers
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError

from arche.models import Profile
from work.models import Works
from .models import Comment, Like, ChatRoom, ChatMessage


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


def chat(request, **kwargs):
    ''' return the chat page '''
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        if ChatRoom.objects.filter(title=room_name).exists():
            return redirect(reverse('room', kwargs={'room_name': room_name}))
        else:
            new_room = ChatRoom.objects.create(title=room_name)
            new_room.save()
            return redirect(reverse('room', kwargs={'room_name': room_name}))
        
    return render(request, 'social/chat.html')


def room(request, room_name):
    room = ChatRoom.objects.get(title=room_name)
    message_count = ChatMessage.objects.count()
    context = {'room': room,
               'message_number': message_count}
    return render(request, 'social/room.html', context)

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']
    room = ChatRoom.objects.get(id=room_id)
    if message != '':
        new_message = ChatMessage.objects.create(content=message,
                                                 user=username,
                                                 room=room)
        new_message.save()
        return HttpResponse('Message sent successfully')

def getMessages(request, room):
    room = ChatRoom.objects.get(title=room)
    messages = ChatMessage.objects.filter(room=room.id).order_by('timestamp')
    return JsonResponse({"messages": list(messages.values())})