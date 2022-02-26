from rest_framework import serializers


class BaseSerializer(serializers.Serializer):
    """ Base Serializer for all Serializer implementations in ebay. """

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class QuerySerializer(BaseSerializer):
    """ Base Serializer for all QuerySerializer implementations in ebay. """


class ErrorResponseSerializer(BaseSerializer):
    """ Error Serializer for our views. """
    error = serializers.DictField(help_text='Possible error codes.')


class ChoiceField(serializers.ChoiceField):

    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return obj
        return self._choices[obj]

    def to_internal_value(self, data):
        # To support inserts with the value
        if data == '' and self.allow_blank:
            return ''

        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail('invalid_choice', input=data)
