'''!/usr/bin/python3
   -*- coding: Utf-8 -'''


from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.contrib.auth.models import User

from work.models import Works


class Comment(models.Model):
	''' User comment model '''
	user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
	date = models.DateField(auto_now_add=True)
	work = models.ForeignKey(Works, on_delete=models.CASCADE, default='0')
	content = models.TextField()

	def __str__(self):
		return self.user.username


LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)


class Like(models.Model):
    '''  '''
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    work = models.ForeignKey(Works, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES,
                             default='Like',
                             max_length=10)

    def __str__(self):
        '''  '''
        return str(self.work)

class ChatRoom(models.Model):
    '''  '''
    title = models.CharField(max_length=255, unique=True, blank=False)
    users = models.ManyToManyField(
        User,
        blank=True,
        help_text="user who are connected to the chat")

    def __str__(self):
        '''  '''
        return self.title

    def connect_user(self, user):
        ''' return true if user is addes to the users list '''
        is_user_added = False
        if not user in self.users.all():
            self.users.add(user)
            self.save()
            is_user_added = True
        elif user in self.users.all():
            is_user_added = True
        return is_user_added

    def disconnect_user(self):
        ''' return true is the user is removed from the users list '''
        is_user_removed = False
        if not user in self.users.all():
            self.users.remove(user)
            self.save()
            is_user_removed = True
        elif user in self.users.all():
            is_user_removed = True
        return is_user_removed

    @property
    def group_name(self):
        ''' return the channels group name that sockets should subscribe 
            to and ge sent messages as they are generated '''
        return f"ChatRoom-{self.id}"


class RoomChatMessageManager(models.Manager):
    '''  '''
    def by_room(self, room):
        '''  '''
        qs = ChatMessage.objects.filter(
            room=room).order_by('-timestamp')
        return qs


class ChatMessage(models.Model):
    ''' public room chat model '''
    user = models.TextField(unique=False, blank=False)
    room = models.ForeignKey(ChatRoom,
                             on_delete=models.CASCADE)

    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField(unique=False, blank=False)

    objects = RoomChatMessageManager()

    def __str__(self):
        '''  '''
        return self.content
