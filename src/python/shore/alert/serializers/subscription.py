from rest_framework import serializers

from alert.models import Subscription
from alert.models.subscription import Frequency
from alert.serializers.base import (
    BaseSerializer,
    ChoiceField,
    QuerySerializer,
)


class SubscriptionSerializer(serializers.ModelSerializer):
    """Serializer for Subscription Model Structure"""

    frequency = ChoiceField(choices=Frequency.choices)

    class Meta:
        model = Subscription
        fields = [
            'id',
            'search_phrase',
            'frequency',
            'is_reverse',
            'user',
        ]


class SubscriptionUpdateSerializer(BaseSerializer):
    """Serializer for updating Subscription."""

    search_phrase = serializers.CharField(help_text='The search phrase of Subscription.', required=True)
    frequency = ChoiceField(help_text='The frequency of the subscription.', choices=Frequency.choices, required=False)


class SubscriptionQuerySerializer(QuerySerializer):
    """ Query Serializer for filtering the Subscription. """
    search_phrase = serializers.CharField(help_text="Search phrase of the alert.", required=False)
    user_id = serializers.UUIDField(help_text='User Id.', required=False)
