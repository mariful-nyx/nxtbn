# Generated by Django 4.2.11 on 2024-12-02 08:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0010_alter_productvariant_stock'),
    ]

    operations = [
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(help_text="Warehouse name. e.g. 'Main Warehouse' or 'Warehouse A' or 'store-1'", max_length=255, unique=True)),
                ('location', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StockMovement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('quantity', models.PositiveIntegerField()),
                ('movement_type', models.CharField(choices=[('PURCHASE', 'Purchase'), ('TRANSFER_IN', 'Transfer In'), ('TRANSFER_OUT', 'Transfer Out'), ('SALE', 'Sale'), ('RETURN', 'Return')], max_length=20)),
                ('note', models.TextField(blank=True, help_text='Additional details about the movement.', null=True)),
                ('from_warehouse', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='outgoing_stock_movements', to='warehouse.warehouse')),
                ('product_variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stock_movements', to='product.productvariant')),
                ('to_warehouse', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='incoming_stock_movements', to='warehouse.warehouse')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('quantity', models.IntegerField(default=0)),
                ('product_variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='warehouse_stocks', to='product.productvariant')),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stocks', to='warehouse.warehouse')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
