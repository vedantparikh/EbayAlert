from uuid import UUID

from django.db import IntegrityError
from django.test import TestCase

from alert.tests.mocks import get_mock_user


class TestUser(TestCase):
    """ Unit test for User model class. """

    def test_user_model_can_be_properly_created(self):
        user = get_mock_user()

        self.assertIsInstance(user.id, UUID)
        self.assertIsInstance(user.email, str)

    def test_email_is_unique(self):
        email = 'test_check@foo.com'
        _ = get_mock_user(email=email)

        with self.assertRaises(IntegrityError):
            get_mock_user(email=email)
