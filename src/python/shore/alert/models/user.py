from uuid import uuid4

from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """ Creates and saves a User with the given email and password. """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_staff_user(self, email, password):
        """ Creates and saves a staff user with the given email and password. """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """ Creates and saves a superuser with the given email and password. """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser):
    """ Custom User model. """

    id = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    email = models.EmailField(unique=True, help_text='User e-mail address.')
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    objects = UserManager()

    def __str__(self) -> str:
        return f'User | {self.email}'
