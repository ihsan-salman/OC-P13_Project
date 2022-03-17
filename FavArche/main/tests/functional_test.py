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
        self.browser.quit()

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
        self.browser.quit()

    def test_add_work(self):
        '''  '''
        self.browser.get(self.INDEX_PAGE_URL)
        self.browser.find_element_by_partial_link_text("Masquer").click()

        self.browser.find_element_by_css_selector("i.fa-sign-in-alt").click()
        self.browser.find_element_by_id(
            "id_username").send_keys('ihsan')
        self.browser.find_element_by_id(
            "id_password").send_keys('far57450')
        self.browser.find_element_by_css_selector("button").click()

        self.browser.find_element_by_css_selector(".fa-book").click()

        self.browser.find_element_by_css_selector(".fa-plus").click()
        self.browser.find_element_by_partial_link_text("ici").click()
        self.browser.find_element_by_css_selector(
            "#id_name").clear()
        self.browser.find_element_by_css_selector(
            "#id_name").send_keys('film')
        self.browser.find_element_by_css_selector(".button-28").click()

        self.browser.find_element_by_name('work_name').send_keys('one piece')
        self.browser.find_element_by_xpath(
            "//select[@name='category']/option[@value='film']").click()
        self.browser.find_element_by_name('wiki').click()
        self.browser.find_element_by_xpath(
            '//input[@type="file"]').send_keys(
            "C://Users/ihsan/Pictures/wallpaper/one_piece.png")
        self.browser.find_element_by_css_selector('.contact_btn').click()

        self.browser.find_element_by_id("work_div").click()
        self.work_name = self.browser.find_element_by_xpath(
            "//div[@id='page_white_div']//h3").get_attribute('innerHTML')
        self.assertEqual(self.work_name, 'One Piece')
        time.sleep(2)
        self.browser.quit()

    def test_social_work_functionality(self):
        ''' test if all social functionality 
            about works funtion correctly '''
        self.browser.get(self.INDEX_PAGE_URL)
        self.browser.find_element_by_partial_link_text("Masquer").click()

        self.browser.find_element_by_css_selector("i.fa-sign-in-alt").click()
        self.browser.find_element_by_id(
            "id_username").send_keys('ihsan')
        self.browser.find_element_by_id(
            "id_password").send_keys('far57450')
        self.browser.find_element_by_css_selector("button").click()

        self.browser.find_element_by_css_selector(".fa-thumbs-up").click()
        self.browser.find_element_by_css_selector(".far").click()

        self.browser.find_element_by_css_selector(
            ".comment_textarea").send_keys('hello')
        self.browser.find_element_by_css_selector(".button-28").click()
        time.sleep(1)
        self.comment_value = self.browser.find_element_by_id(
            "comment_content").get_attribute("innerHTML")
        self.like_number = self.browser.find_element_by_id(
            "like_number").get_attribute("innerHTML")
        self.assertEqual((self.like_number, self.comment_value), 
                         ('1 like', 'hello'))

        self.browser.find_element_by_css_selector(".fa-book").click()
        self.browser.find_element_by_css_selector(".fa-heart").click()
        self.work_name = self.browser.find_element_by_xpath(
            "//div[@id='work_div']//p").get_attribute("innerHTML")
        self.assertEqual(self.work_name, 'One Piece')

    def test_chat(self):
        ''' test if the chat works correctly '''
        self.browser.get(self.INDEX_PAGE_URL)
        self.browser.find_element_by_partial_link_text("Masquer").click()

        self.browser.find_element_by_css_selector("i.fa-sign-in-alt").click()
        self.browser.find_element_by_id(
            "id_username").send_keys('ihsan')
        self.browser.find_element_by_id(
            "id_password").send_keys('far57450')
        self.browser.find_element_by_css_selector("button").click()

        self.browser.find_element_by_partial_link_text("kenshiro57").click()
        self.browser.find_element_by_css_selector(".fa-comments").click()
        self.browser.find_element_by_id("message").send_keys('hello')
        self.browser.find_element_by_xpath("//input[@value='Send']").click()
        time.sleep(3)
        self.message = self.browser.find_element_by_id(
            "message_content").get_attribute("innerHTML")
        self.assertEqual(self.message, 'hello')
        self.browser.quit()
