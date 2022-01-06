'''!/usr/bin/python3
   -*- coding: Utf-8 -'''


from django.db import models

# Create your models here.

class Category(models.Model):
    '''Category model init with fiels'''
    name = models.CharField(max_length=200, unique=True,
                            default='DEFAULT VALUE')

    def __str__(self):
        return str(self.name)


class Works(models.Model):
    '''Works model init with fiels'''
    name = models.CharField(max_length=200,
                            unique=True,
                            default='DEFAULT VALUE')
    web_link = models.URLField()
    image = models.URLField()
    category = models.ForeignKey(Category,
                                 on_delete=models.PROTECT,
                                 null=True,
                                 default=None)

    def __str__(self):
        return str(self.name)


class Favorite(models.Model):
    '''Favorite model init with fiels'''
    works = models.ForeignKey(Works,
                              on_delete=models.PROTECT,
                              related_name='product')

    def __str__(self):
        return str(self.name)
