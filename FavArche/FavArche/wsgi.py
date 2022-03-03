'''!/usr/bin/python3
   -*- coding: Utf-8 -'''

"""
WSGI config for FavArche project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FavArche.settings')

application = get_wsgi_application()
