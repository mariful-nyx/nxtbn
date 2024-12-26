# Generated by Django 4.2.11 on 2024-12-25 11:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0006_alter_purchaseorder_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='purchaseorder',
            options={'ordering': ['-created_at']},
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2024, 12, 25, 11, 4, 2, 717693, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]