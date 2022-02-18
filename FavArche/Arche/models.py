'''!/usr/bin/python3
   -*- coding: Utf-8 -'''


from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user_image',
                              default='default.jpg',
                              blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'
