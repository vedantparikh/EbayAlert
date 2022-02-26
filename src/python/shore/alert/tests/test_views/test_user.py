from uuid import uuid4

from faker import Faker

from django.test import override_settings
from django.urls import reverse
from rest_framework.test import (
    APIClient,
    APITestCase,
)
from rest_framework import status

from alert.models import User
from alert.tests.mocks import get_mock_user

fake = Faker()


@override_settings(ROOT_URLCONF='alert.urls')
class TestUserViewSet(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_mock_user()
        self.response_data = {
            'id': str(self.user.id),
            'email': self.user.email,
        }

    def test_get_user_list(self):
        url = reverse('user-list')
        response = self.client.get(url, format='json')

        self.assertEqual(
            response.json(), [self.response_data]
        )

    def test_retrieve_user(self):
        url = reverse('user-detail', kwargs={
            'uuid': self.user.id
        })
        response = self.client.get(url, format='json')

        self.assertEqual(
            response.json(), self.response_data
        )

    def test_retrieve_non_existing_user(self):
        url = reverse('user-detail', kwargs={
            'uuid': uuid4()
        })
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_user(self):
        payload = {
            'email': fake.unique.email()
        }
        url = reverse('user-list')
        response = self.client.post(url, data=payload, format='json')
        data = response.json()
        data.pop('id')
        self.assertEqual(data, payload)

    def test_create_user_with_already_exists_email(self):
        payload = {
            'email': self.user.email,
        }
        url = reverse('user-list')
        response = self.client.post(url, data=payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_user(self):
        payload = {
            'email': 'updated_email@foobar.com',
        }
        url = reverse('user-detail', kwargs={
            'uuid': self.user.id
        })
        response = self.client.put(url, data=payload, format='json')
        data = response.json()
        data.pop('id')

        self.assertEqual(data, payload)

    def test_update_with_invalid_payload_user(self):
        payload = {
            'email': 'test'
        }
        url = reverse('user-detail', kwargs={
            'uuid': self.user.id
        })
        response = self.client.put(url, data=payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_user(self):
        url = reverse('user-detail', kwargs={
            'uuid': self.user.id
        })
        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_non_existing_user(self):
        url = reverse('user-detail', kwargs={
            'uuid': uuid4()
        })
        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
