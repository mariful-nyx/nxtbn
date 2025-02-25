# Generated by Django 4.2.11 on 2024-12-15 21:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0005_warehouse_is_default'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockreservation',
            name='transferred_to',
            field=models.ForeignKey(help_text='Destination warehouse for stock transfer during order fulfillment.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transfers', to='warehouse.warehouse'),
        ),
    ]
