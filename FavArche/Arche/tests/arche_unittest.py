'''!/usr/bin/python3
   -*- coding: Utf-8 -'''


from django.urls import reverse
from django.test import TestCase
from django.http import HttpResponse
from django.contrib.auth.models import User

from arche.forms import EditProfileForm
from arche.models import Profile
from work.models import Works, Category

from urllib.parse import urlencode

""" Django Unittest including medthods, views and database """
""" Using Testcase library from Django Test """

class IndexPageTestCase(TestCase):
    ''' Index page test class '''
    def setUp(self):
        ''' init all variables to cover view method statements '''
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        self.user = User.objects.create_user(**self.credentials)
        Profile.objects.create(user=self.user)
        self.category = Category.objects.create(name='test')
        self.test_work = Works.objects.create(
            name='test_work',
            user=self.user,
            image='test.jpg',
            description='test description',
            category=self.category)

    def test_index_page_returns_200(self):
        ''' Test if the Http request returns 200 code statue 
            and the template used '''
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'favarche/index.html')

    def test_work_data_post_with_login(self):
        ''' test if the post method returns 200 with user logged in'''
        self.client.post(reverse('login'), self.credentials, follow=True)
        response = self.client.post(reverse('home'), 
                                    data={'work_id': self.test_work.id,
                                          'comment': 'blabla'})
        self.assertEqual(response.status_code, 200)

    def test_work_data_post(self):
        ''' test if the post method returns 200 with user isn' connected'''
        response = self.client.post(reverse('home'), 
                                    data={'work_id': self.test_work.id,
                                          'comment': 'blabla'})
        self.assertEqual(response.status_code, 200)


class ContactPageTestCase(TestCase):
    '''  contact page test class '''
    def test_about__page_returns_200(self):
        ''' Test if the Http request returns 200 code statue 
            and the template used '''
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'favarche/informative/contact.html')

    def test_contact_post_returns_200(self):
        ''' test if the mail data returns 200 code statue '''
        response = self.client.post('/contact/', 
                                    data={'email': 'email@example.com',
                                          'subject': 'subject',
                                          'message': 'message'})
        self.assertEqual(response.status_code, 302)

    def test_mail_data_returns_404(self):
        ''' test if the mail data returns 404 code statue '''
        response = self.client.post(reverse('contact'), 
                                    data={'email': '',
                                          'subject': '',
                                          'message': ''})
        self.assertEqual(response.status_code, 404)


class AboutUsPageTestCase(TestCase):
    ''' About us page test class '''
    def test_about_us_page_returns_200(self):
        ''' Test if the Http request returns 200 code statue 
            and the template used '''
        response = self.client.get(reverse('about_us'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'favarche/informative/about.html')


class FunctionalityPageTestCase(TestCase):
    ''' functionality page test class '''
    def test_functionality_page_returns_200(self):
        ''' Test if the Http request returns 200 code statue 
            and the template used '''
        response = self.client.get(reverse('functionality'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'favarche/informative/functionality.html')


class CategoryPageTestCase(TestCase):
    ''' category page test class '''
    def test__page_returns_200(self):
        ''' Test if the Http request returns 200 code statue 
            and the template used '''
        response = self.client.get(reverse('category'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'favarche/informative/category.html')


class Page404TestCase(TestCase):
    ''' 404 page test class '''
    def test__page_returns_404(self):
        ''' test if the Http request returns 404 code statue 
            and the template used '''
        response = self.client.get('/udhduehd/')
        self.assertEqual(response.status_code, 404)


class AccountPageTestCase(TestCase):
    '''Account page test class'''
    def setUp(self):
        '''Init all needed data for the test'''
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        self.user = User.objects.create_user(**self.credentials)
        Profile.objects.create(user=self.user)

    def test_login(self):
        '''Test if the Http request returns 200 when the user is logged'''
        # send login data
        self.client.post(reverse('login'), self.credentials, follow=True)
        response = self.client.get(reverse('my_account'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'favarche/account/my_account.html')


class EditProfilePageTestCase(TestCase):
    '''edit account page test class'''
    def setUp(self):
        '''Init all needed data for the test'''
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)

    def test_login(self):
        '''Test if the Http request returns 200 when the user is logged'''
        # send login data
        self.client.post(reverse('login'),
                         self.credentials,
                         follow=True)
        response = self.client.get(reverse('edit_account'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'favarche/account/edit_account.html')

    def test_form_validation(self):
        ''' test if the edit profile form is valid '''
        self.form_data = {'username': 'test_user',
                     'email': 'i@i.com',
                     'first_name': 'test',
                     'last_name': 'user'}
        form = EditProfileForm(data=self.form_data)
        self.assertTrue(form.is_valid())

