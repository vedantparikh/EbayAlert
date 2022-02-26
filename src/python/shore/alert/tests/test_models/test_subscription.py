from uuid import UUID
from datetime import datetime

from django.test import TestCase

from alert.models import User
from alert.tests.mocks import get_mock_subscription


class TestSubscription(TestCase):
    """ Unit test for Subscription model class. """

    def test_subscription_model_can_be_properly_created(self):
        subscription = get_mock_subscription()

        self.assertIsInstance(subscription.id, UUID)
        self.assertIsInstance(subscription.search_phrase, str)
        self.assertIsInstance(subscription.frequency, int)
        self.assertIsInstance(subscription.user, User)
        self.assertIsInstance(subscription.created_at, datetime)
        self.assertIsInstance(subscription.updated_at, datetime)

        # delete
        subscription.delete()
        self.assertEqual(subscription.is_deleted, True)
