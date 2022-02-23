'''!/usr/bin/python3
   -*- coding: Utf-8 -'''


import time
from django.test import LiveServerTestCase
from selenium import webdriver

""" Django Functional Test with Selenium library """
"""" automatising user's interaction with the website """


class TestProject(LiveServerTestCase):
    ''' All functional Django Test class '''
    def setUp(self):
        ''' Init all Functional test '''
        # Path to edge webdriver
        self.browser = webdriver.Edge(
            r"D:\Python projects\Django\msedgedriver.exe")
        self.INDEX_PAGE_URL = 'http://127.0.0.1:8000/'

    def test_index_page_title(self):
        ''' Little functional test to make sure about the url page contents '''
        # Get the selected page contents
        self.browser.get(self.INDEX_PAGE_URL)
        # Test comparison between the current url and the test's expected url
        self.assertEqual(self.browser.title, 'Favarche')
        # Close the current page
        self.browser.quit()