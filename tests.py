import unittest
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import random
import json
import time
import os

from selenium.webdriver.support import expected_conditions as EC


class wait_for_loading(object):
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        try:
            print("xxxxxx")
            print(driver)
            print(self.locator)
            element = EC._find_element(driver, self.locator)
            return False if "loading" in element.get_attribute("class") else True
        except:
            return False


driver = webdriver.Chrome()


class MyTest(unittest.TestCase):
    def setUp(self):
        driver.get("http://localhost:8800/")

    @unittest.skip("not now")
    def test_signup(self):
        signup_btn = driver.find_element_by_class_name("signup-btn")
        signup_btn.click()

        usernameInput = driver.find_element_by_id("username")
        usernameInput.send_keys("Moustafa")

        emailInput = driver.find_element_by_id("email")
        emailInput.send_keys("Moustafa@gmail.com")

        passwordInput = driver.find_element_by_id("password")
        passwordInput.send_keys("111111")

        retype_passwordInput = driver.find_element_by_id("retype_password")
        retype_passwordInput.send_keys("111111")

        retype_passwordInput.send_keys(Keys.RETURN)

        self.assertEqual(driver.current_url, "http://localhost:8800/")

    def test_signin(self):
        signup_btn = driver.find_element_by_class_name("signin-btn")
        signup_btn.click()

        usernameInput = driver.find_element_by_id("username")
        usernameInput.send_keys("Moustafa")

        passwordInput = driver.find_element_by_id("password")
        passwordInput.send_keys("111111")

        passwordInput.send_keys(Keys.RETURN)

        self.assertEqual(driver.current_url, "http://localhost:8800/")

        driver.find_element_by_class_name("header-logo").click()

    def test_follow(self):
        for btn in driver.find_elements_by_class_name("toggle-follow"):
            btn.click()

        #driver.find_element_by_class_name("header-logo").click()

        for rating in driver.find_elements_by_class_name("rating"):
            rating.find_element_by_xpath(".//i[3]").click()

        self.assertEqual(driver.current_url, "http://locfalhost:8800/")

    @classmethod
    def tearDownClass(cls):
        # driver.quit()
        pass


unittest.main()
