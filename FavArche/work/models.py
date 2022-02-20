'''!/usr/bin/python3
   -*- coding: Utf-8 -'''


from django.db import models
from django.utils.timezone import now

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
