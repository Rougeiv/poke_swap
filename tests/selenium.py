import unittest
from app import create_app, db
from config import TestConfig
from app.models import User
from unittest import TestCase

class SeleniumTestCase(TestCase):

    def setUp(self):
        testApp = create_app(TestConfig)
        self.app_context = testApp.app_context()
        self.app_context.push()
        db.create_all()

    def tearDOwn(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()