# Generated by Django 4.2.11 on 2024-10-23 03:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shipping', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='shippingrate',
            unique_together={('shipping_method', 'country', 'weight_min', 'weight_max')},
        ),
    ]
