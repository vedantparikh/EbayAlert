# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
# from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
# from django.contrib.auth.forms import UserChangeForm as DjangoUserChangeForm
# from django.contrib.auth.forms import ValidationError
# from django.forms.fields import EmailField
#
# from alert.models import (
#     Product,
#     Subscription,
#     User,
# )
#
#
# class UserCreationForm(DjangoUserCreationForm):
#     """ User creation form using email as username """
#
#     class Meta:
#         model = User
#         fields = ("username",)
#         field_classes = {
#             'username': EmailField
#         }
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.email = user.get_username().lower()
#         user.username = user.get_username().lower()
#         if commit:
#             user.save()
#         return user
#
#
# class UserChangeForm(DjangoUserChangeForm):
#     """ User change form which validates that email can't be different than username """
#
#     def clean(self):
#         is_staff = self.cleaned_data["is_staff"]
#         # username and email are not required to be same for superusers.
#         if not is_staff:
#             username = self.cleaned_data["username"]
#             email = self.cleaned_data["email"]
#             if username.lower() != email.lower():
#                 raise ValidationError("Email can not be different than username!")
#         return super().clean()
#
#
# @admin.register(User)
# class UserAdmin(DjangoUserAdmin):
#     """Admin interface for managing Users."""
#     list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
#     filter_horizontal = ('groups', 'user_permissions')
#
#     form = UserChangeForm
#     add_form = UserCreationForm
#
#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         if not request.user.is_superuser:
#             return qs.filter(is_superuser=False)
#         return qs
#
#     def get_fieldsets(self, request, obj=None):
#         if not obj:
#             return self.add_fieldsets
#
#         if request.user.is_superuser:
#             perm_fields = ('is_active', 'is_staff', 'is_superuser',
#                            'groups', 'user_permissions')
#             important_dates = ('Important dates', {
#                 'fields': ('last_login', 'date_joined')
#             })
#         else:
#             perm_fields = ('is_active', 'is_staff')
#             important_dates = (None, {
#                 'fields': ()
#             })
#
#         return [(None, {
#             'fields': ('username', 'password')
#         }),
#                 ('Personal info', {
#                     'fields': ('first_name', 'last_name', 'email')
#                 }),
#                 ('Permissions', {
#                     'fields': perm_fields
#                 }),
#                 important_dates,
#                 ]
#
#
# @admin.register(Subscription)
# class SubscriptionAdmin(admin.ModelAdmin):
#     """ Admin interface for managing Subscription. """
#
#     list_display = (
#         'id',
#         'search_phrase',
#         'frequency',
#         'user',
#         'is_reverse',
#         'last_frequency_change_at',
#     )
#
#
# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     """ Admin interface for managing Product. """
#
#     list_display = (
#         'id',
#         'name',
#         'price',
#         'subscription',
#         'user',
#     )
