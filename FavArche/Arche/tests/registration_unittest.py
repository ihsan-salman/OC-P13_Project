'''!/usr/bin/python3
   -*- coding: Utf-8 -'''


from unittest import mock

from django.urls import reverse
from django.test import TestCase
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm

from urllib.parse import urlencode

from registration import views
from registration.forms import CustomAuthenticationForm, RegisterForm


""" Django Unittest including medthods, views and database """
""" Using Testcase library from Django Test """

class LoginPageTestCase(TestCase):
    '''Login page test class'''
    def test_login_page_returns_200(self):
        '''Test of the Http request returns 200'''
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def setUp(self):
        '''Init all needed data to test the user's login'''
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        self.user = User.objects.create_user(**self.credentials)

    def test_login(self):
        '''Test if the user is logged after the login step'''
        # send login data
        response = self.client.post(
            reverse('login'),
                    self.credentials,
                    follow=True)
        # should be logged in now
        self.assertTrue(response.context['user'].is_authenticated)


class CreateAccountPageTestCase(TestCase):
    ''' Create Account page test class '''
    def test_create_page_returns_200(self):
        ''' Test of the Http request returns 200 '''
        response = self.client.get(reverse('create_account'),)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/create_account.html')

    def test_create_account_ok(self):
        ''' Test of acccount creation '''
        response = self.client.post(reverse('create_account'), data={
            'email': 'i@i.com',
            'username': 'iiii',
            'first_name': 'aaaa',
            'last_name': 'oooo',
            'password1': 'azeqsd00'})
        self.assertEqual(response.status_code, 200)

    def test_form_validation(self):
        ''''''
        password = make_password("azeqsd00")
        form = RegisterForm(data={
            'email': 'i@i.com',
            'username': 'iiiidbuybeb',
            'first_name': 'aaaedubefva',
            'last_name': 'oooohsshhsh',
            'password1': password,
            'password2': password})
        self.assertTrue(form.is_valid())


class ChangePasswordPageTestCase(TestCase):
    def setUp(self):
        '''Init all needed data to test the user's login'''
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)

    ''' Change password test case '''
    def test_password_change(self):
        ''' Test of the Http request returns 200 '''
        self.client.post(reverse('login'),
                                    self.credentials,
                                    follow=True)
        response = self.client.get(reverse('change_password'),)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/change_password.html')

        response = self.client.post(reverse('change_password'),
                                     data={'old_password': 'test_user',
                                           'new_password1': 'gfnfnffnfn',
                                           'new_password2': 'gfnfnfn'})
        self.assertEqual(response.status_code, 200)



class Page404TestCase(TestCase):
    ''' 404 page test class '''
    def test__page_returns_404(self):
        ''' test if the Http request returns 404 code statue 
            and the template used '''
        response = self.client.get('/udhduehd/')
        self.assertEqual(response.status_code, 404)
