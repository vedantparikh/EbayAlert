from uuid import uuid4

from django.conf import settings
from django.db import models
from django.db.models import QuerySet

from alert.models.managers import (
    DefaultSoftDeleteManager,
    DeletedSoftDeleteManager,
    NotDeletedSoftDeleteManager,
    SoftDeleteModelMixin,
)
from alert.models.querysets import SoftDeleteQuerySet

User = settings.AUTH_USER_MODEL


class SubscriptionQuerySet(SoftDeleteQuerySet):
    """ Query-Set for Subscription. """

    def filter_by_search_phrase(self, search_phrase: str) -> QuerySet:
        """Returns List of subscriptions filter by search phrase."""

        return self.filter(search_phrase=search_phrase)

    def subscription_exists(self, search_phrase, user) -> bool:
        """ Returns bool if subscription instance already exists. """

        return self.filter(search_phrase=search_phrase, user=user).exists()


class Frequency(models.IntegerChoices):
    TWO = 2, 'Two'
    FIFTEEN = 15, 'Fifteen'
    THIRTY = 30, 'Thirty'


class Subscription(SoftDeleteModelMixin):
    """ Subscription model. """

    id = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    search_phrase = models.CharField(max_length=255, help_text='Name of the product.')
    frequency = models.IntegerField(choices=Frequency.choices, help_text='Price of the product.')
    is_reverse = models.BooleanField(default=True, help_text='Whether to show results in reverse order.')

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='subscription_user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = NotDeletedSoftDeleteManager.from_queryset(SubscriptionQuerySet)()
    deleted_objects = DeletedSoftDeleteManager.from_queryset(SubscriptionQuerySet)()
    all_objects = DefaultSoftDeleteManager.from_queryset(SubscriptionQuerySet)()

    class Meta:
        default_manager_name = 'all_objects'
        app_label = 'alert'
        db_table = 'alert_subscription'

    def __str__(self) -> str:
        return f'Subscription | {self.search_phrase} | {self.user}'
