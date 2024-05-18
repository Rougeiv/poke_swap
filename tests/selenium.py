from datetime import time
import multiprocessing
from selenium import webdriver
from app import create_app, db
from config import TestConfig
from app.models import User
from unittest import TestCase

localhost = "http://localhost:5000"

class SeleniumTestCase(TestCase):

    def setUp(self):
        testApp = create_app(TestConfig)
        self.app_context = testApp.app_context()
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

    def test_signup(self):
        time.sleep(10)
        self.assertTrue(True)

        loginEle = self.driver.find_element(BY.ID, "login")
        loginEle.send_keys("01349324")