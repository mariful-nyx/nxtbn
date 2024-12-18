# Generated by Django 4.2.11 on 2024-12-13 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0027_alter_order_options_order_reservation_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='reservation_status',
            field=models.CharField(choices=[('RESERVED', 'Reserved'), ('RELEASED', 'Released'), ('FAILED', 'Failed'), ('NOT_RESERVED', 'Not Reserved')], default='NOT_RESERVED', max_length=20),
        ),
    ]