# Generated by Django 3.2.12 on 2022-02-26 19:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('alert', '0002_adds_subscription_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('is_deleted', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Name of the product.', max_length=255)),
                ('price', models.DecimalField(decimal_places=2, help_text='Price of the product.', max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('subscription', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_subscription', to='alert.subscription')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'alert_product',
                'default_manager_name': 'all_objects',
            },
            managers=[
                ('all_objects', django.db.models.manager.Manager()),
            ],
        ),
    ]