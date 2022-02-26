from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User Model Structure"""

    class Meta:
        model = User
        fields = [
            'id',
            'email',
        ]
