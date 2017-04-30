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

driver = webdriver.Chrome()

class MyTest(unittest.TestCase):
    def setUp(self):
        driver.get("http://localhost:8800/")

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

        for btn in driver.find_elements_by_class_name("toggle-follow"):
            btn.click()

        wait = WebDriverWait(driver, 10)
        results = wait.until(EC.presence_of_all_elements_located((By.LINK_TEXT, '#duckbar_static>li.zcm__item'),""))

        driver.find_element_by_class_name("header-logo").click()

        for rating in driver.find_elements_by_class_name("rating"):
            rating.find_element_by_xpath(".//i[3]").click()

    @classmethod
    def tearDownClass(cls):
        #driver.quit()
        pass


unittest.main()