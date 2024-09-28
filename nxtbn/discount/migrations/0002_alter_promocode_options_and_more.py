# Generated by Django 4.2.11 on 2024-09-28 02:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_alter_address_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0003_product_tax_class'),
        ('discount', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='promocode',
            options={'verbose_name': 'Promo Code', 'verbose_name_plural': 'Promo Codes'},
        ),
        migrations.AddField(
            model_name='promocode',
            name='min_purchase_amount',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Minimum total purchase amount required to use the promo code.', max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='promocode',
            name='min_purchase_period',
            field=models.DurationField(blank=True, help_text='Time period (e.g., 30 days) within which the minimum purchase amount should be met.', null=True),
        ),
        migrations.AddField(
            model_name='promocode',
            name='new_customers_only',
            field=models.BooleanField(default=False, help_text='If set, only newly registered customers can use this promo code.'),
        ),
        migrations.AddField(
            model_name='promocode',
            name='redemption_limit',
            field=models.PositiveIntegerField(blank=True, help_text='Maximum number of times this promo code can be redeemed.', null=True),
        ),
        migrations.AddField(
            model_name='promocode',
            name='usage_limit_per_customer',
            field=models.PositiveIntegerField(default=1, help_text='Maximum number of times a single customer can redeem this promo code.'),
        ),
        migrations.CreateModel(
            name='PromoCodeUsage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('applied_at', models.DateTimeField(auto_now_add=True, help_text='The timestamp when the promo code was applied.')),
                ('order', models.ForeignKey(help_text='The order associated with the use of this promo code.', on_delete=django.db.models.deletion.CASCADE, to='order.order')),
                ('promo_code', models.ForeignKey(help_text='The promo code that was applied to the order.', on_delete=django.db.models.deletion.CASCADE, to='discount.promocode')),
                ('user', models.ForeignKey(help_text='Select the customer who redeemed this promo code.', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PromoCodeProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(help_text='The product eligible for this promo code.', on_delete=django.db.models.deletion.CASCADE, to='product.product')),
                ('promo_code', models.ForeignKey(help_text='The promo code that applies to specific products.', on_delete=django.db.models.deletion.CASCADE, to='discount.promocode')),
            ],
            options={
                'verbose_name': 'Promo Code Product',
                'verbose_name_plural': 'Promo Code Products',
                'unique_together': {('promo_code', 'product')},
            },
        ),
        migrations.CreateModel(
            name='PromoCodeCustomer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.ForeignKey(help_text='The customer who is eligible to use this promo code.', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('promo_code', models.ForeignKey(help_text='The promo code that is restricted to specific customers.', on_delete=django.db.models.deletion.CASCADE, to='discount.promocode')),
            ],
            options={
                'verbose_name': 'Promo Code Customer',
                'verbose_name_plural': 'Promo Code Customers',
                'unique_together': {('promo_code', 'customer')},
            },
        ),
        migrations.AddField(
            model_name='promocode',
            name='applicable_products',
            field=models.ManyToManyField(blank=True, help_text='Specify products that must be purchased to use the promo code.', related_name='promo_codes', through='discount.PromoCodeProduct', to='product.product'),
        ),
        migrations.AddField(
            model_name='promocode',
            name='specific_customers',
            field=models.ManyToManyField(blank=True, help_text='Specify users who are eligible for this promo code.', related_name='promo_codes', through='discount.PromoCodeCustomer', to=settings.AUTH_USER_MODEL),
        ),
    ]