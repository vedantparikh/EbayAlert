from rest_framework import serializers

from alert.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User Model Structure"""

    class Meta:
        model = User
        fields = [
            'id',
            'email',
        ]
