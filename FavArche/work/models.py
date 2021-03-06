'''!/usr/bin/python3
   -*- coding: Utf-8 -'''


from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

from ckeditor.fields import RichTextField

# Create your models here.


class Category(models.Model):
    '''Category model init with fiels'''
    name = models.CharField(max_length=150, unique=True,
                            default='Nom')
    description = RichTextField(blank=True, null=True)

    def __str__(self):
        return str(self.name)


class Works(models.Model):
    '''Works model init with fiels'''
    name = models.CharField(max_length=200,
                            default='DEFAULT VALUE')
    image = models.ImageField(
            upload_to='work_image/', blank=True,
            null=False, default='default_work.png')
    category = models.ForeignKey(Category,
                                 on_delete=models.PROTECT,
                                 null=True)
    time = models.DateTimeField(default=now, editable=False)
    description = RichTextField(blank=True, null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    liked = models.ManyToManyField(
            User, default=None, blank=True, related_name='work_post_like')
    fav = models.ManyToManyField(
            User, default=None, blank=True, related_name='work_post_fav')

    def __str__(self):
        return str(self.name)

    @property
    def num_likes(self):
        '''  '''
        return self.liked.all().count()


class Favorite(models.Model):
    '''Favorite model init with fiels'''
    favorite_works = models.OneToOneField(
            Works, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.favorite_works)
