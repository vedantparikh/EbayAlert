from uuid import uuid4

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """ Custom User model. """

    id = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    email = models.EmailField(unique=True, help_text='User e-mail address.')

    def __str__(self) -> str:
        return f'User | {self.email}'
