from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from django.contrib.auth.forms import UserChangeForm as DjangoUserChangeForm
from django.contrib.auth.forms import ValidationError
from django.forms.fields import EmailField

from alert.models import (
    Product,
    Subscription,
)

User = get_user_model()


class UserCreationForm(DjangoUserCreationForm):
    """ User creation form using email as username """

    class Meta:
        model = User
        fields = ("email",)
        field_classes = {
            'email': EmailField
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = user.get_username().lower()
        user.username = user.get_username().lower()
        if commit:
            user.save()
        return user


class UserChangeForm(DjangoUserChangeForm):
    """ User change form which validates that email can't be different than username """

    def clean(self):
        is_staff = self.cleaned_data["is_staff"]
        # username and email are not required to be same for superusers.
        if not is_staff:
            username = self.cleaned_data["username"]
            email = self.cleaned_data["email"]
            if username.lower() != email.lower():
                raise ValidationError("Email can not be different than username!")
        return super().clean()


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Admin interface for managing Users."""

    list_display = ('id', 'email')
    form = UserChangeForm
    add_form = UserCreationForm
    list_filter = ()
    filter_horizontal = ()
    ordering = ()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.admin:
            return qs.filter(admin=False)
        return qs

    def get_fieldsets(self, request, obj=None):

        if request.user.admin:
            important_dates = ('Important dates', {
                'fields': ('last_login',)
            })
        else:
            important_dates = (None, {
                'fields': ()
            })

        return [(None, {
            'fields': ('email', 'password')
        }),
                ('Personal info', {
                    'fields': ('email',)
                }),
                important_dates,
                ]


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """ Admin interface for managing Subscription. """

    list_display = (
        'id',
        'search_phrase',
        'frequency',
        'user',
        'is_reverse',
        'is_deleted',
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """ Admin interface for managing Product. """

    list_display = (
        'id',
        'product_id',
        'name',
        'price',
        'subscription',
        'is_deleted',
    )
