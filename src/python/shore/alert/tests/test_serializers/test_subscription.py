from uuid import uuid4

from django.test import TestCase

from alert.serializers import (
    SubscriptionSerializer,
    SubscriptionQuerySerializer,
)
from alert.tests.mocks import get_mock_user


class TestSubscriptionSerializer(TestCase):
    def setUp(self) -> None:
        self.user = get_mock_user()

    def test_subscription_serializer(self):
        data = {
            'id': str(uuid4),
            'search_phrase': 'test_search_phrase',
            'frequency': 'Two',
            'last_frequency_change_at': '2021-09-14T14:00:33.715211Z',
            'is_reverse': True,
            'is_deleted': False,
            'user': self.user.pk
        }
        serializer = SubscriptionSerializer(data=data)
        self.assertTrue(serializer.is_valid(raise_exception=True))

    def test_subscription_query_serializer(self):
        query_params = {
            'search_phrase': 'random search',
        }
        serializer = SubscriptionQuerySerializer(data=query_params)
        self.assertTrue(serializer.is_valid(raise_exception=True))
