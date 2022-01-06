'''!/usr/bin/python3
   -*- coding: Utf-8 -'''


from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User

""" Django Unittest including medthods, views and database """
""" Using Testcase library from Django Test """

class IndexPageTestCase(TestCase):
    ''' Index page test class '''
    def test_index_page_returns_200(self):
        ''' Test if the Http request returns 200 code statue 
            and the template used '''
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'favarche/index.html')
