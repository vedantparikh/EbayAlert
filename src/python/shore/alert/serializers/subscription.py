from rest_framework import serializers

from alert.models import Subscription
from alert.serializers.base import QuerySerializer


class SubscriptionSerializer(serializers.ModelSerializer):
    """Serializer for Subscription Model Structure"""

    class Meta:
        model = Subscription
        fields = [
            'id',
            'search_phrase',
            'frequency',
            'is_reverse',
            'last_frequency_change_at',
            'user',
        ]


class SubscriptionQuerySerializer(QuerySerializer):
    search_phrase = serializers.EmailField(
        help_text="Search phrase of the alert.", required=False
    )
