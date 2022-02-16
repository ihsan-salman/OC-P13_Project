'''!/usr/bin/python3
   -*- coding: Utf-8 -'''


from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    '''Category model init with fiels'''
    name = models.CharField(max_length=150, unique=True,
                            default='Nom')
    description = models.CharField(max_length=500, default='Description')

    def __str__(self):
        return str(self.name)


class Works(models.Model):
    '''Works model init with fiels'''
    name = models.CharField(max_length=200,
                            default='DEFAULT VALUE')
    web_link = models.URLField()
    image = models.ImageField(upload_to='work_image/', unique=True)
    category = models.ForeignKey(Category,
                                 on_delete=models.PROTECT,
                                 null=True,
                                 default=None)
    time = models.DateTimeField(default=now, editable=False)
    description = models.CharField(max_length=500, default='Description')
    username = models.CharField(max_length=100, default='None')

    def __str__(self):
        return str(self.name)


class Favorite(models.Model):
    '''Favorite model init with fiels'''
    works = models.ForeignKey(Works,
                              on_delete=models.PROTECT,
                              related_name='product')

    def __str__(self):
        return str(self.name)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user_image',
                              default='default.jpg',
                              blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'
