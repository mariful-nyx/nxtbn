# Generated by Django 4.2.11 on 2024-12-14 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0004_stocktransfer_stocktransferitem_delete_stockmovement'),
    ]

    operations = [
        migrations.AddField(
            model_name='warehouse',
            name='is_default',
            field=models.BooleanField(default=False, help_text='Only one warehouse can be default'),
        ),
    ]
