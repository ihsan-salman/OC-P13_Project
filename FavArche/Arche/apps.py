'''!/usr/bin/python3
   -*- coding: Utf-8 -'''


from django.apps import AppConfig


class ArcheConfig(AppConfig):
    ''' App defalut config class '''
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'arche'
