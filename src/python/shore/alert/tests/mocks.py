from typing import Union
from datetime import datetime

from faker import Faker

from alert.models import (
    Product,
    Subscription,
    User,
)

fake = Faker()


def get_mock_user(email: str = None) -> User:
    return User.objects.create(email=email or fake.unique.email())


def get_mock_subscription(
        search_phrase: str = None,
        frequency: int = 2,
        user: User = None,
) -> Subscription:
    return Subscription.objects.create(
        search_phrase=search_phrase or fake.text(21),
        frequency=frequency,
        user=user or get_mock_user(),
    )


def get_mock_product(
        product_id: str = None,
        name: str = None,
        price: Union[int, float] = None,
        subscription: Subscription = None,
) -> Product:
    return Product.objects.create(
        product_id=product_id or fake.text(31),
        name=name or fake.text(21),
        price=price or fake.pyint(),
        subscription=subscription or get_mock_subscription(),
    )
