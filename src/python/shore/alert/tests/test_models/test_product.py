import decimal
from uuid import UUID
from datetime import datetime

from django.test import TestCase

from alert.models import (
    Subscription,
    User,
)
from alert.tests.mocks import (
    get_mock_product,
    get_mock_subscription,
    get_mock_user,
)


class TestProduct(TestCase):
    """ Unit test for Product model class. """

    def test_product_model_can_be_properly_created(self):
        user = get_mock_user(email='foobar@bar.com')
        subscription = get_mock_subscription(user=user)
        product = get_mock_product(subscription=subscription)

        self.assertIsInstance(product.id, UUID)
        self.assertIsInstance(product.product_id, str)
        self.assertIsInstance(product.name, str)
        self.assertIsInstance(product.price, int)
        self.assertIsInstance(product.subscription, Subscription)
        self.assertIsInstance(product.created_at, datetime)
        self.assertIsInstance(product.updated_at, datetime)

        # delete
        product.delete()
        self.assertEqual(product.is_deleted, True)
