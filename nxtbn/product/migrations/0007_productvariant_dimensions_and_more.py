# Generated by Django 4.2.11 on 2024-10-07 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_productvariant_allow_backorder_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productvariant',
            name='dimensions',
            field=models.CharField(blank=True, choices=[('MM', 'Millimeter'), ('CM', 'Centimeter'), ('M', 'Meter'), ('IN', 'Inch'), ('FT', 'Feet')], help_text='Format: Height x Width x Depth', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='productvariant',
            name='dimensions_value',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
