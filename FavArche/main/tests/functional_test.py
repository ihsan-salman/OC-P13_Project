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
        self.ACCOUNT_PAGE_URL = 'http://127.0.0.1:8000/mon_compte/'

    def test_index_page_title(self):
        ''' Little functional test to make sure about the url page contents '''
        # Get the selected page contents
        self.browser.get(self.INDEX_PAGE_URL)
        # Test comparison between the current url and the test's expected url
        self.assertEqual(self.browser.title, 'Favarche')
        # Close the current page
        self.browser.quit()

    def test_my_account_page(self):
        ''' test if the user can log in and get account page, and change her 
            information correctly '''
        self.browser.get(self.INDEX_PAGE_URL)
        # Hide toolbar
        self.browser.find_element_by_partial_link_text("Masquer").click()
        # Click button event
        self.browser.find_element_by_css_selector("i.fa-sign-in-alt").click()
        # Search the Html element by id and input the value
        self.browser.find_element_by_id(
            "id_username").send_keys('ihsan')
        self.browser.find_element_by_id(
            "id_password").send_keys('far57450')
        self.browser.find_element_by_css_selector("button").click()
        self.browser.find_element_by_css_selector("i.fa-user").click()
        self.assertEqual(self.browser.current_url, self.ACCOUNT_PAGE_URL)
        self.browser.find_element_by_id("edit_account").click()
        self.browser.find_element_by_id(
            "id_first_name").send_keys('ihsan')
        self.browser.find_element_by_id(
            "id_last_name").send_keys('salman')
        self.browser.find_element_by_css_selector("button").click()
        self.first_name_value = self.browser.find_element_by_id("first_name")
        self.last_name_value = self.browser.find_element_by_id("last_name")
        self.first_name_value = self.first_name_value.get_attribute(
            "innerHTML")
        self.last_name_value = self.last_name_value.get_attribute(
            "innerHTML")
        self.assertEqual([self.first_name_value, self.last_name_value,],
                         ['ihsan', 'salman'])

    def test_contact_email(self):
        ''' test if the user can send an email to contact admin '''
        self.browser.get(self.INDEX_PAGE_URL)
        self.browser.find_element_by_partial_link_text("Masquer").click()
        self.browser.find_element_by_partial_link_text("Contact").click()
        self.browser.find_element_by_name("email").send_keys('i@i.com')
        self.browser.find_element_by_name("subject").send_keys('nothing')
        self.browser.find_element_by_name("message").send_keys('nothing')
        self.browser.find_element_by_css_selector("button").click()
        self.assertEqual(self.browser.current_url, self.INDEX_PAGE_URL)



