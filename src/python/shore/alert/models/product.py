from uuid import uuid4

from django.db import models
from django.db.models import QuerySet

from alert.models.managers import (
    DefaultSoftDeleteManager,
    DeletedSoftDeleteManager,
    NotDeletedSoftDeleteManager,
    SoftDeleteModelMixin,
)
from alert.models.querysets import SoftDeleteQuerySet
from alert.models.subscription import Subscription


class ProductQuerySet(SoftDeleteQuerySet):
    """ Query-Set for Product. """

    def filter_by_name(self, name: str) -> QuerySet:
        return self.filter(name=name)


class Product(SoftDeleteModelMixin):
    """ Product model. """

    id = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    product_id = models.CharField(max_length=255, help_text='The Product Id.')
    name = models.CharField(max_length=255, null=True, blank=True, help_text='Name of the product.')
    price = models.DecimalField(decimal_places=2, max_digits=10, help_text='Price of the product.')
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, null=True,
                                     related_name='product_subscription')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = NotDeletedSoftDeleteManager.from_queryset(ProductQuerySet)()
    deleted_objects = DeletedSoftDeleteManager.from_queryset(ProductQuerySet)()
    all_objects = DefaultSoftDeleteManager.from_queryset(ProductQuerySet)()

    class Meta:
        default_manager_name = 'all_objects'
        app_label = 'alert'
        db_table = 'alert_product'

    def __str__(self) -> str:
        return f'Subscription | {self.name} | {self.price}'
