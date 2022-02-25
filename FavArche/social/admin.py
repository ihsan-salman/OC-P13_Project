'''!/usr/bin/python3
   -*- coding: Utf-8 -'''


from django.contrib import admin
from .models import Comment


admin.site.register(Comment)