'''!/usr/bin/python3
   -*- coding: Utf-8 -'''


from unittest import mock

from django.urls import reverse
from django.test import TestCase
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm

from main.models import Profile
from work.models import Works, Category
from social.models import Comment, ChatRoom


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
    ''' like page test case '''
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


class ChatTestCase(TestCase):
    ''' chat view test case '''
    def setUp(self):
        '''Init all needed data to test the user's login'''
        self.credentials1 = {
            'username': 'testuser',
            'password': 'secret'}
        self.user1 = User.objects.create_user(**self.credentials1)
        self.client.post(reverse('login'), self.credentials1, follow=True)

    def test_page_returns_404(self, **kwargs):
        response = self.client.get(reverse('chat',
                                           kwargs={'username': self.user1.username}))
        self.assertEqual(response.status_code, 404)

    def test_page_returns_302(self, **kwargs):
        self.credentials2 = {
            'username': 'testuser2',
            'password': 'secret2'}
        self.user2 = User.objects.create_user(**self.credentials2)
        response = self.client.get(reverse('chat',
                                           kwargs={'username': self.user2.username}))
        self.assertEqual(response.status_code, 302)


class RoomPageTestCase(TestCase):
    ''' Room page test case '''
    def setUp(self):
        '''Init all needed data to test the user's login'''
        self.credentials1 = {
            'username': 'testuser',
            'password': 'secret'}
        self.user1 = User.objects.create_user(**self.credentials1)
        self.client.post(reverse('login'), self.credentials1, follow=True)
        self.credentials2 = {
            'username': 'testuser2',
            'password': 'secret2'}
        self.user2 = User.objects.create_user(**self.credentials2)
        response = self.client.get(reverse('chat',
                                           kwargs={'username': self.user2.username}))

    def test_page_returns_200(self, **kwargs):
        ''' test if the page returns 200 http status code '''
        response = self.client.get(reverse('room', kwargs={'id': 3}))
        self.assertEqual(response.status_code, 200)


class SendMessagesTestCase(TestCase):
    ''' send message test case '''
    def setUp(self):
        '''Init all needed data to test the user's login'''
        self.credentials1 = {
            'username': 'testuser',
            'password': 'secret'}
        self.user1 = User.objects.create_user(**self.credentials1)
        self.client.post(reverse('login'), self.credentials1, follow=True)
        self.credentials2 = {
            'username': 'testuser2',
            'password': 'secret2'}
        self.user2 = User.objects.create_user(**self.credentials2)
        response = self.client.get(reverse('chat',
                                           kwargs={'username': self.user2.username}))

    def test_response_returns_200(self):
        ''' test if the response returns 200 '''
        response = self.client.post(reverse('send_message'),
                                   data={'message': 'ok',
                                         'username': self.user2.username,
                                         'room_id': 4})
        self.assertEqual(response.status_code, 200)


class GetMessagesTestCase(TestCase):
    ''' get message test case '''
    def setUp(self):
        '''Init all needed data to test the user's login'''
        self.credentials1 = {
            'username': 'testuser',
            'password': 'secret'}
        self.user1 = User.objects.create_user(**self.credentials1)
        self.client.post(reverse('login'), self.credentials1, follow=True)
        self.credentials2 = {
            'username': 'testuser2',
            'password': 'secret2'}
        self.user2 = User.objects.create_user(**self.credentials2)
        response = self.client.get(reverse('chat',
                                           kwargs={'username': self.user2.username}))

    def test_response_returns_200(self, **kwargs):
        ''' test if the response returns 200 '''
        response = self.client.get(reverse('get_message', kwargs={'id': 2}))
        self.assertEqual(response.status_code, 200)
