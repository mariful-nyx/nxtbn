# Generated by Django 4.2.11 on 2024-12-01 11:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_remove_productvariant_variant_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productvariant',
            name='weight_unit',
        ),
    ]
