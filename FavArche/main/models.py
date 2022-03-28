'''!/usr/bin/python3
   -*- coding: Utf-8 -'''


from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    ''' Profile model class '''
    user = user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user_image',
                              default='default.jpg',
                              blank=True)
