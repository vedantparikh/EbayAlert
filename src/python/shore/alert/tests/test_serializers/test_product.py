from uuid import uuid4

from django.test import TestCase

from alert.serializers import (
    ProductSerializer,
    ProductQuerySerializer,
)
from alert.tests.mocks import (
    get_mock_user,
    get_mock_subscription,
    get_mock_product,
)


class TestProductSerializer(TestCase):

    def setUp(self) -> None:
        self.user = get_mock_user()
        self.subscription = get_mock_subscription(user=self.user)

    def test_product_serializer(self):
        data = {
            'id': str(uuid4),
            'product_id': 'unique_product_number',
            'name': 'test_name',
            'price': 21.22,
            'subscription': self.subscription.pk,
            'is_deleted': False,
        }
        serializer = ProductSerializer(data=data)
        self.assertTrue(serializer.is_valid(raise_exception=True))

    def test_product_query_serializer(self):
        query_params = {
            'name': 'random search',
            'subscription_id': str(uuid4()),
        }
        serializer = ProductQuerySerializer(data=query_params)
        self.assertTrue(serializer.is_valid(raise_exception=True))
