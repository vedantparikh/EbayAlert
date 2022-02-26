from uuid import uuid4

from django.test import TestCase

from alert.models import User
from alert.serializers import UserSerializer


class TestUserSerializer(TestCase):

    def test_serializer(self):
        data = {
            'id': str(uuid4()),
            'email': 'foo@bar.com'
        }

        # with display_name present
        instance = User(**data)
        serializer = UserSerializer(data=data, instance=instance)
        serializer.is_valid(raise_exception=True)

        self.assertEqual(serializer.data, data)
