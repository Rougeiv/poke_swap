from datetime import time
import multiprocessing
from selenium import webdriver
# from selenium.webdriver.common.by import By
from app import create_app, db
from config import TestConfig
from app.models import User
from unittest import TestCase

localhost = "http://localhost:5000"

class SeleniumTestCase(TestCase):

    def setUp(self):
        self.testApp = create_app(TestConfig)
        self.app_context = self.testApp.app_context()
        self.app_context.push()
        db.create_all()

        self.server_process = multiprocessing.Process(target=self.testApp.run)
        self.server_process.start()

        self.driver = webdriver.Chrome()
        self.driver.get(localhost)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

        self.server_process.terminate()

    def test_login(self):
        time.sleep(1)
        loginEle = self.driver.find_element(webdriver.common.By.ID, "username")
        loginEle.send_keys("MythicFJGHKJ")

        loginEle = self.driver.find_element(webdriver.common.By.ID, "password")
        loginEle.send_keys("Password1!")

        loginEle = self.driver.find_element(webdriver.common.By.ID, "submit")
        loginEle.click()

        
        self.assertEqual(self.driver.current_url, localhost + "login")
        time.sleep(10)

