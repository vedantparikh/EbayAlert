from rest_framework import serializers

from alert.models import Product
from alert.serializers.base import QuerySerializer


class ProductSerializer(serializers.ModelSerializer):
    """ Serializer for Product Model Structure. """

    class Meta:
        model = Product
        fields = [
            'id',
            'product_id',
            'name',
            'price',
            'subscription',
        ]


class ProductUpdateSerializer(QuerySerializer):
    """ Serializer for updating the Product Model. """
    product_id = serializers.CharField(help_text="Id of the Product.", required=False)
    name = serializers.CharField(help_text="Name of the product.", required=False)
    price = serializers.DecimalField(
        max_digits=10, decimal_places=2, help_text="Name of the product.", required=False
    )


class ProductQuerySerializer(QuerySerializer):
    """ Query Serializer for filtering the Products. """
    subscription_id = serializers.UUIDField(help_text="Id of the Subscription.", required=False)
    name = serializers.CharField(help_text="Name of the product.", required=False)
