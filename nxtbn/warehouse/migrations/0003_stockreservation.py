# Generated by Django 4.2.11 on 2024-12-13 08:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0002_stock_reserved'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockReservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('quantity', models.PositiveIntegerField()),
                ('purpose', models.CharField(help_text="Purpose of the reservation. e.g. 'Pending Order', 'Blocked Stock', 'Pre-booked Stock'", max_length=50)),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='warehouse.stock')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]