# from datetime import time
# import multiprocessing
# from selenium import webdriver
# # from selenium.webdriver.common.by import By
# from app import create_app, db
# from config import TestConfig
# from app.models import User
# from unittest import TestCase

# localhost = "http://localhost:5000"

# class SeleniumTestCase(TestCase):

#     def setUp(self):
#         self.testApp = create_app(TestConfig)
#         self.app_context = self.testApp.app_context()
#         self.app_context.push()
#         db.create_all()

#         self.server_process = multiprocessing.Process(target=self.testApp.run)
#         self.server_process.start()

#         self.driver = webdriver.Chrome()
#         self.driver.get(localhost)

#     def run_server(self):
#         self.app.run(port=5000)

#     def create_user(self, username, email, password):
#         user = User(username=username, email=email)
#         user.set_password(password)
#         db.session.add(user)
#         db.session.commit()

#     def tearDown(self):
#         db.session.remove()
#         db.drop_all()
#         self.app_context.pop()

#         self.server_process.terminate()

#     def test_login_success(self):
#         self.create_user('testuser', 'test@example.com', 'password')
#         self.driver.get('http://localhost:5000/login')
#         sleep(1)

#         username_input = self.driver.find_element(webdriver.common.By.ID, "username")
#         password_input = self.driver.find_element(webdriver.common.By.ID, "password")
#         login_button = self.driver.find_element(webdriver.common.By.ID, "submit")

#         username_input.send_keys("Mythic")
#         password_input.send_keys("Password1!")
#         login_button.click()

        
#         sleep(1)
#         self.assertIn('http://localhost:5000/', self.driver.current_url)


#     def test_login_missing_user(self):
#         sleep(1)

#         username_input = self.driver.find_element(webdriver.common.By.ID, "username")
#         password_input = self.driver.find_element(webdriver.common.By.ID, "password")
#         login_button = self.driver.find_element(webdriver.common.By.ID, "submit")

#         username_input.send_keys("MythicFJGHKJ")
#         password_input.send_keys("Password1!")
#         login_button.click()

#         # messages = self.driver.find_elements(webdriver.common.By.ID, "")
#         sleep(1)
#         # self.assertIn('http://localhost:5000/', self.driver.current_url)
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import os
import unittest
import multiprocessing
from app import create_app, db
from config import TestConfig
from app.models import User

class SeleniumTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        self.server_process = multiprocessing.Process(target=self.run_server)
        self.server_process.start()
        sleep(1)  # give the server some time to start

        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()
        self.server_process.terminate()
        self.app_context.pop()
        db.session.remove()
        db.drop_all()

    def run_server(self):
        self.app.run(port=5001)

    def create_user(self, username, email, password):
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

    def test_login(self):
        #self.create_user('testuser', 'test@example.com', 'password')
        self.driver.get('http://localhost:5000/login')
        sleep(1)
        
        self.driver.maximize_window()

        # Add a sleep to ensure the page loads completely (if necessary)
        sleep(5)


        element = self.driver.find_element(By.XPATH, "/html/body/nav/div/ul/li[5]/a")
        element.click()

        # Wait for the username input element and enter the username
        username_element = self.driver.find_element(By.XPATH, "/html/body/div/div/div/div/div/div/div/div/form/p[1]/input")
        username_element.send_keys("Mythicrif")
        
        # Sleep for 2 seconds
        sleep(2)

        # Wait for the password input element and enter the password
        password_element = self.driver.find_element(By.XPATH, "/html/body/div/div/div/div/div/div/div/div/form/p[2]/input")
        password_element.send_keys("SuperCoolPassword!!")
        
        sleep(1)
        self.assertIn('http://localhost:5000/', self.driver.current_url)

    def test_navigation(self):
        self.create_user('testuser', 'test@example.com', 'password')
        self.driver.get('http://localhost:5000/login')
        sleep(1)

        username_input = self.driver.find_element(By.ID, "username")
        password_input = self.driver.find_element(By.ID, "password")        
        login_button = self.driver.find_element(By.ID, 'submit')

        username_input.send_keys('testuser')
        password_input.send_keys('password')
        login_button.click()
        
        sleep(1)
        
        # Navigate to Trade Offer
        self.driver.find_element(By.LINK_TEXT, 'Trade').click()
        username_input = self.driver.find_element(By.ID, "username")
        sleep(1)
        self.assertIn('http://localhost:5000/trade_offer', self.driver.current_url)

    def test_trade_offer_page(self):
        self.create_user('testuser', 'test@example.com', 'password')
        self.driver.get('http://localhost:5000/login')
        sleep(1)

        username_input = self.driver.find_element(By.ID,'username')
        password_input = self.driver.find_element(By.ID, 'password')
        login_button = self.driver.find_element(By.ID, 'submit')

        username_input.send_keys('testuser')
        password_input.send_keys('password')
        login_button.click()
        
        sleep(1)

        # Navigate to Trade Offer
        self.driver.find_element(By.LINK_TEXT, 'Trade').click()
        sleep(1)
        
        # Verify Trade Offer Page
        self.assertIn('http://localhost:5000/trade_offer', self.driver.current_url)
        self.assertIn('Catch Pokemon', self.driver.page_source)

if __name__ == "__main__":
    unittest.main()
