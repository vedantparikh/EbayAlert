from uuid import uuid4
from datetime import datetime

from faker import Faker

from django.test import override_settings
from django.urls import reverse
from rest_framework.test import (
    APIClient,
    APITestCase,
)
from rest_framework import status

from alert.tests.mocks import (
    get_mock_product,
    get_mock_user,
    get_mock_subscription,
)

fake = Faker()


@override_settings(ROOT_URLCONF='alert.urls')
class TestProductViewSet(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_mock_user()
        self.subscription = get_mock_subscription(user=self.user)
        self.product = get_mock_product(subscription=self.subscription, price=32.11)
        self.response_data = {
            'id': str(self.product.id),
            'product_id': str(self.product.product_id),
            'name': self.product.name,
            'price': str(self.product.price),
            'subscription': str(self.product.subscription.pk),
        }

    def test_get_product_list(self):
        url = reverse('product-list')
        response = self.client.get(url, format='json')

        self.assertEqual(
            response.json(), [self.response_data]
        )

    def test_get_product_list_filter_by_name(self):
        name = self.product.name
        url = reverse('product-list')
        response = self.client.get(url + f'?name={name}', format='json')

        self.assertEqual(
            response.json(), [self.response_data]
        )

    def test_get_product_list_filter_by_subscription_id(self):
        subscription_id = self.product.subscription.pk
        url = reverse('product-list')
        response = self.client.get(url + f'?subscription_id={subscription_id}', format='json')

        self.assertEqual(
            response.json(), [self.response_data]
        )

    def test_get_product_list_filter_by_name_and_subscription_id(self):
        name = self.product.name
        subscription_id = self.product.subscription.pk
        url = reverse('product-list')
        response = self.client.get(url + f'?name={name}&subscription_id={subscription_id}', format='json')

        self.assertEqual(
            response.json(), [self.response_data]
        )

    def test_retrieve_product(self):
        url = reverse('product-detail', kwargs={
            'uuid': self.product.id
        })
        response = self.client.get(url, format='json')

        self.assertEqual(
            response.json(), self.response_data
        )

    def test_retrieve_non_existing_product(self):
        url = reverse('product-detail', kwargs={
            'uuid': uuid4()
        })
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_product(self):
        payload = {
            'product_id': fake.text(31),
            'name': fake.text(31),
            'price': '21.44',
        }
        url = reverse('product-list')
        response = self.client.post(url, data=payload, format='json')
        data = response.json()

        self.assertEqual(data['product_id'], payload['product_id'])
        self.assertEqual(data['name'], payload['name'])
        self.assertEqual(data['price'], payload['price'])

    def test_create_user_with_wrong_payload(self):
        payload = {
            'name': fake.text(31),
            'price': 2,
        }
        url = reverse('user-list')
        response = self.client.post(url, data=payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_product(self):
        payload = {
            'product_id': fake.text(31),
            'name': 'updated_name',
            'price': '2.00',
        }
        url = reverse('product-detail', kwargs={
            'uuid': self.product.id
        })
        response = self.client.put(url, data=payload, format='json')
        data = response.json()

        self.assertEqual(data['product_id'], payload['product_id'])
        self.assertEqual(data['name'], payload['name'])
        self.assertEqual(data['price'], payload['price'])

    def test_update_with_invalid_payload_product(self):
        payload = {
            'product_id': True,
            'name': 12.31,
        }
        url = reverse('product-detail', kwargs={
            'uuid': self.product.id
        })
        response = self.client.put(url, data=payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_product(self):
        url = reverse('product-detail', kwargs={
            'uuid': self.product.id
        })
        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_non_existing_product(self):
        url = reverse('product-detail', kwargs={
            'uuid': uuid4()
        })
        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
