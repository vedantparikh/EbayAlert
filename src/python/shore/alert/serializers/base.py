from rest_framework import serializers


class BaseSerializer(serializers.Serializer):
    """Base Serializer for all Serializer implementations in ebay."""

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class QuerySerializer(BaseSerializer):
    """Base Serializer for all QuerySerializer implementations in ebay."""


class ErrorResponseSerializer(BaseSerializer):
    error = serializers.DictField(help_text='Possible error codes.')
