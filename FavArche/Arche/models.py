'''!/usr/bin/python3
   -*- coding: Utf-8 -'''


from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    '''Category model init with fiels'''
    name = models.CharField(max_length=200, unique=True,
                            default='None')

    def __str__(self):
        return str(self.name)


class Works(models.Model):
    '''Works model init with fiels'''
    name = models.CharField(max_length=200,
                            unique=True,
                            default='DEFAULT VALUE')
    web_link = models.URLField()
    hotel_Main_Img = models.ImageField(upload_to='images/')
    category = models.ForeignKey(Category,
                                 on_delete=models.PROTECT,
                                 null=True,
                                 default=None)
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
    image = models.ImageField(default='default.jpg', blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'
