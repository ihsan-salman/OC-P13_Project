'''!/usr/bin/python3
   -*- coding: Utf-8 -'''


from django.db import models
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
