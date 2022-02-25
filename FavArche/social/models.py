'''!/usr/bin/python3
   -*- coding: Utf-8 -'''


from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User


class Comment(models.Model):
	''' User comment model '''
