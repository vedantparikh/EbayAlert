from uuid import uuid4
from unittest import mock

from faker import Faker

from django.test import override_settings
from django.urls import reverse
from rest_framework.test import (
    APIClient,
    APITestCase,
)
from rest_framework import status

from alert.tests.mocks import (
    get_mock_user,
    get_mock_subscription,
)

fake = Faker()


@override_settings(ROOT_URLCONF='alert.urls')
class TestSubscriptionViewSet(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_mock_user()
        self.subscription = get_mock_subscription(
            user=self.user
        )
        self.response_data = {
            'id': str(self.subscription.id),
            'search_phrase': self.subscription.search_phrase,
            'frequency': 'Two',
            'is_reverse': self.subscription.is_reverse,
            'user': str(self.user.pk),
        }

    def test_get_subscription_list(self):
        url = reverse('subscription-list')
        response = self.client.get(url, format='json')

        self.assertEqual(
            response.json(), [self.response_data]
        )

    def test_get_subscription_list_filter_with_search_phrase(self):
        search_phrase = self.subscription.search_phrase
        url = reverse('subscription-list')
        response = self.client.get(url + f'?search_phrase={search_phrase}', format='json')

        self.assertEqual(
            response.json(), [self.response_data]
        )

    def test_retrieve_subscription(self):
        url = reverse('subscription-detail', kwargs={
            'uuid': self.subscription.id
        })
        response = self.client.get(url, format='json')

        self.assertEqual(
            response.json(), self.response_data
        )

    def test_retrieve_non_existing_subscription(self):
        url = reverse('subscription-detail', kwargs={
            'uuid': uuid4()
        })
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @mock.patch('alert.views.subscription.create_product')
    @mock.patch('alert.views.subscription.create_task')
    def test_create_subscription(self, mock_create_task, mock_create_product):
        mock_create_task.return_value = None
        mock_create_product.return_value = None
        payload = {
            'search_phrase': fake.text(31),
            'frequency': 'Two',
        }
        url = reverse('subscription-list')
        response = self.client.post(url, data=payload, format='json')
        data = response.json()

        self.assertEqual(data['search_phrase'], payload['search_phrase'])
        self.assertEqual(data['frequency'], payload['frequency'])
        self.assertTrue(data['is_reverse'])
        mock_create_task.assert_called()
        mock_create_product.assert_called()

    def test_create_user_with_wrong_payload(self):
        payload = {
            'search_phrase': fake.text(31),
            'frequency': 2,
        }
        url = reverse('user-list')
        response = self.client.post(url, data=payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @mock.patch('alert.views.subscription.create_product')
    @mock.patch('alert.views.subscription.create_task')
    @mock.patch('alert.views.subscription.delete_periodic_task')
    def test_update_subscription(self, mock_delete_periodic_task, mock_create_task, mock_create_product):
        mock_delete_periodic_task.return_value = None
        mock_create_task.return_value = None
        mock_create_product.return_value = None
        payload = {
            'search_phrase': 'updated_search_phrase',
            'frequency': 'Two',
        }
        url = reverse('subscription-detail', kwargs={
            'uuid': self.subscription.id
        })
        response = self.client.put(url, data=payload, format='json')
        data = response.json()

        self.assertEqual(data['search_phrase'], payload['search_phrase'])
        self.assertEqual(data['frequency'], payload['frequency'])
        mock_create_task.assert_called()
        mock_create_product.assert_called()
        mock_delete_periodic_task.assert_called()

    def test_update_with_invalid_payload_subscription(self):
        payload = {
            'frequency': 2,
            'search_phrase': 'update_phrase',
        }
        url = reverse('subscription-detail', kwargs={
            'uuid': self.subscription.id
        })
        response = self.client.put(url, data=payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @mock.patch('alert.views.subscription.delete_periodic_task')
    def test_delete_subscription(self, mock_delete_periodic_task):
        mock_delete_periodic_task.return_value = None
        url = reverse('subscription-detail', kwargs={
            'uuid': self.subscription.id
        })
        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_delete_periodic_task.assert_called()

    def test_delete_non_existing_subscription(self):
        url = reverse('subscription-detail', kwargs={
            'uuid': uuid4()
        })
        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
