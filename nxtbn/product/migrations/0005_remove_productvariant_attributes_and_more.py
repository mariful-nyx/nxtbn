# Generated by Django 4.2.11 on 2024-11-07 09:45

from django.db import migrations, models
import nxtbn.core.models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_alter_product_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productvariant',
            name='attributes',
        ),
        migrations.AddField(
            model_name='productvariant',
            name='internal_metadata',
            field=models.JSONField(blank=True, default=dict, null=True, validators=[nxtbn.core.models.no_nested_values]),
        ),
        migrations.AddField(
            model_name='productvariant',
            name='metadata',
            field=models.JSONField(blank=True, default=dict, null=True, validators=[nxtbn.core.models.no_nested_values]),
        ),
        migrations.AlterField(
            model_name='product',
            name='related_to',
            field=models.ManyToManyField(blank=True, help_text='Related products. For example, if you have a product that is a t-shirt, each product can have variants by size and color. In this case, you can relate all the products by color. This field is not intended for recommendation engines.', to='product.product'),
        ),
    ]
