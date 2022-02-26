from uuid import uuid4

from django.db import models

from alert.models.managers import (
    DefaultSoftDeleteManager,
    DeletedSoftDeleteManager,
    NotDeletedSoftDeleteManager,
    SoftDeleteModelMixin,
)
from alert.models.querysets import SoftDeleteQuerySet
from alert.models.subscription import Subscription
from alert.models.user import User


class ProductQuerySet(SoftDeleteQuerySet):
    """ Query-Set for Product. """

    pass


class Product(SoftDeleteModelMixin):
    """ Product model. """

    id = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=255, help_text='Name of the product.')
    price = models.DecimalField(decimal_places=2, max_digits=10, help_text='Price of the product.')
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, null=True,
                                     related_name='product_subscription')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='product_user')
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
