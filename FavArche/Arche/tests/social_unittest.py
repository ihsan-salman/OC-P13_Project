'''!/usr/bin/python3
   -*- coding: Utf-8 -'''


from unittest import mock

from django.urls import reverse
from django.test import TestCase
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm

from arche.models import Profile
from work.models import Works, Category
from social.models import Comment


class OtherAccountPageTestCase(TestCase):
    '''other account page test class'''
    def setUp(self):
        '''Init all needed data to test the user's login'''
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        self.user = User.objects.create_user(**self.credentials)
        Profile.objects.create(user=self.user)

    def test_page_returns_200(self, **kwargs):
        '''Test of the Http request returns 200'''
        response = self.client.post(reverse('other_accounts',
                                    kwargs={'username': 'testuser'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'social/account.html')


class DeleteCommentTestCase(TestCase):
    ''' delete account test case '''
    def setUp(self):
        '''Init all needed data to test the user's login'''
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        self.user = User.objects.create_user(**self.credentials)
        self.category = Category.objects.create(name='test')
        self.test_work = Works.objects.create(
            name='test_work',
            user=self.user,
            image='test.jpg',
            description='test description',
            category=self.category)
        self.comment = Comment.objects.create(
            user=self.user,
            work=self.test_work,
            content='test')

    def test_delete_comment(self):
        ''' test if the comment is deleted '''
        response = self.client.post(reverse('delete_comment'),
                                    data={'comment_id': self.comment.id})
        self.assertEqual(response.status_code, 200)


class LikeTestCase(TestCase):
    ''' like test case '''
    def setUp(self):
        '''Init all needed data to test the user's login'''
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

    def test_delete_comment(self):
        ''' test if the comment is deleted '''
        self.client.post(reverse('login'), self.credentials, follow=True)
        response = self.client.post(reverse('Like'),
                                    data={'work_id': self.test_work.id})
        self.assertEqual(response.status_code, 200)
