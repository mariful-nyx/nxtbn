# Generated by Django 4.2.11 on 2024-12-05 15:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0023_rename_email_address_address_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='total_price_in_customer_currency',
        ),
        migrations.RemoveField(
            model_name='orderlineitem',
            name='total_price_in_customer_currency',
        ),
    ]
