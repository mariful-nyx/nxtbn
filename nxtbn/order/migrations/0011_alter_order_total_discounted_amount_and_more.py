# Generated by Django 4.2.11 on 2024-10-06 13:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0010_rename_total_shipping_fee_order_total_shipping_cost_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total_discounted_amount',
            field=models.BigIntegerField(blank=True, default=0, help_text='Total amount of the order after applying discounts in cents, stored in the base currency.', null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_shipping_cost',
            field=models.BigIntegerField(blank=True, default=0, help_text='Total shipping amount of the order in cents, stored in the base currency.', null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_tax',
            field=models.BigIntegerField(blank=True, default=0, help_text='Total tax amount of the order in cents, stored in the base currency.', null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
