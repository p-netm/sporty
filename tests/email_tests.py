"""
Simple Few unittest to check the erorr handling when saving a user email
"""
import unittest
from sqlalchemy.exc import InvalidRequestError
from app import create_app
from app.email import db, SubscribedEmail, FlushError, IntegrityError, InvalidRequestError, add_email


class EmailTests(unittest.TestCase):
    """refer module docstring"""
    def setUp(self):
        #set up database
        app = create_app('testing')
        app_context = app.app_context()
        app_context.push()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.drop_all()

    def test_add_email_for_one_valid_email(self):
        response = add_email("asdaf@mail.com")
        self.assertTrue(len(SubscribedEmail.query.all()))
        self.assertIsInstance(response, dict)

    def test_add_email_for_valid_duplicates_email(self):
        add_email("asdaf@mail.com")
        self.assertEqual(len(SubscribedEmail.query.all()), 1)
        response = add_email("asdaf@mail.com")
        self.assertEqual(len(SubscribedEmail.query.all()), 1)
        self.assertIn('status', response.keys())
        self.assertEqual('bad', response['status'])

