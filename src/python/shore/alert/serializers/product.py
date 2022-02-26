from rest_framework import serializers

from alert.models import Product
from alert.serializers.base import QuerySerializer


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product Model Structure"""

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'price',
            'subscription',
            'user',
        ]


class ProductQuerySerializer(QuerySerializer):
    user_id = serializers.UUIDField(
        help_text="Id of the User.", required=False
    )
    name = serializers.CharField(
        help_text="Name of the product.", required=False
    )
