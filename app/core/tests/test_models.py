"""
Test for models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

class modelTest(TestCase):
    """ Test models """

    def test_create_user_with_email_successful(self):
        """ Test createing a user with an email is successful """
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)

        # user user.check to check through the hashing algorith
        self.assertTrue(user.check_password(password))
