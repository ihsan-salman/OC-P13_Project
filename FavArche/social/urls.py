'''!/usr/bin/python3
   -*- coding: Utf-8 -'''


from django.urls import path

from . import views

urlpatterns = [
   path('compte/<str:username>', views.account, name='other_accounts'),
   path('', views.delete_comment, name='delete_comment'),
   path('like/', views.like, name='Like'),
   path('chat/<str:username>/', views.chat, name='chat'),
   path('chatroom/<str:id>/', views.room, name='room'),
   path('send', views.send, name='send_message'),
   path('getMessages/<str:id>/', views.getMessages, name='get_message'),
]
