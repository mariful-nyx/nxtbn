# Generated by Django 4.2.11 on 2024-12-10 18:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0011_remove_productvariant_color_code_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productvariant',
            name='is_preorder',
        ),
        migrations.RemoveField(
            model_name='productvariant',
            name='stock',
        ),
    ]
