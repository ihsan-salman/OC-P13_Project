'''!/usr/bin/python3
   -*- coding: Utf-8 -'''


from django.urls import reverse
from django.test import TestCase
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.core.files.uploadedfile import SimpleUploadedFile

from unittest.mock import patch

from main.models import Profile
from work.models import Works, Category
from work.forms import CategoryForm, EditCategoryForm, ImageForm
from work.helper import wiki_page

class PersonalUserPageTestCase(TestCase):
    ''' PersonalUser page test class '''
    def setUp(self):
        ''' init all variables to cover view method statements '''
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        self.user = User.objects.create_user(**self.credentials)
        Profile.objects.create(user=self.user)
        self.category = Category.objects.create(name='test')

    def test_personal_page_returns_200_with_0_work(self):
        ''' Test if the Http request returns 200 code statue 
            and the template used '''
        self.client.post(reverse('login'), self.credentials, follow=True)
        response = self.client.get(reverse('personal_works'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'works/personal_works.html')

    def test_personal_page_returns_200_with_1_work(self):
        ''' Test if the Http request returns 200 code statue 
            and the template used '''
        self.client.post(reverse('login'), self.credentials, follow=True)
        self.test_work = Works.objects.create(
            name='test_work',
            user=self.user,
            image='test.jpg',
            description='test description',
            category=self.category)
        response = self.client.get(reverse('personal_works'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'works/personal_works.html')


class EditWorkPageTestCase(TestCase):
    ''' Edit work page test case '''
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

    def test_get_method_page_returns_200(self, **kwargs):
        ''' test the page get method is used '''
        self.client.post(reverse('login'), self.credentials, follow=True)
        response = self.client.get(reverse('edit_work',
                                    kwargs={'work_name': 'test_work'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'works/edit_work.html')

    def test_post_method_page_returns_302(self, **kwargs):
        ''' test the page post method is used '''
        self.client.post(reverse('login'), self.credentials, follow=True)
        response = self.client.post(reverse('edit_work',
                                            kwargs={
                                                'work_name': 'test_work'}),
                                    data={'work_name': 'test_work2',
                                          'category': 'test',
                                          'description': 'description'})
        self.assertEqual(response.status_code, 302)


class AddWorkPageTestCase(TestCase):
    ''' add work page test case '''
    def setUp(self):
        ''' init all variables to cover view method statements '''
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        self.user = User.objects.create_user(**self.credentials)
        self.client.post(reverse('login'), self.credentials, follow=True)

    def return_error(self):
        error = """Le nom de votre oeuvre ne permet pas 
                   de trouver une url compatible avec 
                   les données de Wikipedia..."""
        return error

    def test_work_add_returns_200_with_category(self):
        ''' test if adding work returns 200 '''
        self.category = Category.objects.create(name='test')
        self.data_form = {'image': 'image.jpg'}
        form = ImageForm(data=self.data_form)
        response = self.client.post(reverse('add_works'),
                                    data={'form': form,
                                          'work_name': 'test_work',
                                          'category': 'test',
                                          'description': ''})
        self.assertEqual(response.status_code, 200)

    def test_work_add_returns_200_without_category(self):
        ''' test if adding work returns 200 '''
        response = self.client.get(reverse('add_works'))
        self.assertEqual(response.status_code, 200)



class AddCategoryPageTestCase(TestCase):
    ''' add category page test case '''
    def setUp(self):
        ''' init all variables to cover view method statements '''
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        self.user = User.objects.create_user(**self.credentials)

    def test_category_add_returns_200(self):
        ''' test if the category is correctly added '''
        self.client.post(reverse('login'), self.credentials, follow=True)
        self.data_form = {'name': 'test', 'description': 'description'}
        form = CategoryForm(data=self.data_form)
        response = self.client.post(reverse('add_category'),
                                    data={'form' : form})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(form.is_valid())


class WorkDetailPageTestCase(TestCase):
    ''' work detail page page test case '''

    def setUp(self):
        ''' init all variables to cover view method statements '''
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        self.user = User.objects.create_user(**self.credentials)
        self.category = Category.objects.create(name='test')

    def test_page_returns_200(self, **kwargs):
        ''' test if the work detail page returns 200 Http code statue '''
        self.test_work = Works.objects.create(
            name='test_work',
            user=self.user,
            image='test.jpg',
            description='test description',
            category=self.category)
        response = self.client.get(reverse('work_details',
                                           kwargs={'work_name': 
                                                   self.test_work.name}))
        self.assertEqual(response.status_code, 200)

    def test_page_returns_404(self, **kwargs):
        ''' test if the work detail page returns 200 Http code statue '''
        response = self.client.get(reverse('work_details',
                                           kwargs={'work_name': 
                                                   'test_work'}))
        self.assertEqual(response.status_code, 404)


class FavoriteWorksPageTestCase(TestCase):
    ''' Favorite page test case '''
    def setUp(self):
        ''' init all variables to cover view method statements '''
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        self.user = User.objects.create_user(**self.credentials)
        self.client.post(reverse('login'), self.credentials, follow=True)

    def test_page_returns_200(self):
        response = self.client.get(reverse('fav_works'))
        self.assertEqual(response.status_code, 200)


class EditCategoryPageTestCase(TestCase):
    ''' Edit Category page test case '''
    def setUp(self):
        ''' init all variables to cover view method statements '''
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        self.user = User.objects.create_user(**self.credentials)
        self.client.post(reverse('login'), self.credentials, follow=True)
        self.category = Category.objects.create(name='test')

    def test_page_returns_200_with_form(self, **kwargs):
        ''' test if the edit category page returns 200 Http code statue '''
        self.form_data = {'description': 'description'}
        form = EditCategoryForm(data=self.form_data, instance=self.category)
        response = self.client.post(reverse('edit_category',
                                           kwargs={'category_name': 
                                                   self.category.name}),
                                   data={'form': form})
        self.assertEqual(response.status_code, 302)

    def test_page_returns_200_without_form(self, **kwargs):
        ''' test if the edit category page returns 200 Http code statue '''
        form = EditCategoryForm(instance=self.category)
        response = self.client.get(reverse('edit_category',
                                           kwargs={'category_name': 
                                                   self.category.name}),
                                   data={'form': form})
        self.assertEqual(response.status_code, 200)


class GetWikiDataTestCase(TestCase):
    ''' Test get_wiki view '''
    def return_wiki(self):
        return ['www.test_work.com', 'test_work']

    @patch("work.views.wiki_page", return_wiki)
    def test_get_wiki_returns_200(self):
        response = self.client.post(reverse('wiki_data'),
                                   data={'work_name': 'test_work'},
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
