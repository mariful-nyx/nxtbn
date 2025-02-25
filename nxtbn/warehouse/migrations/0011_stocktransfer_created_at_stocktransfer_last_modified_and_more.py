# Generated by Django 4.2.11 on 2025-01-17 10:20

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0010_stocktransferitem_received_quantity_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='stocktransfer',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2025, 1, 17, 10, 20, 26, 559696, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stocktransfer',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='stocktransferitem',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stocktransferitem',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
