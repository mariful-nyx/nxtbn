# Generated by Django 4.2.11 on 2024-09-23 03:52

from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaxClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'verbose_name': 'Tax Class',
                'verbose_name_plural': 'Tax Classes',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='TaxRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('state', models.CharField(blank=True, max_length=2, null=True)),
                ('rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('is_active', models.BooleanField(default=True)),
                ('exempt_products', models.ManyToManyField(blank=True, to='product.product')),
                ('tax_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tax.taxclass')),
            ],
            options={
                'verbose_name': 'Tax Rate',
                'verbose_name_plural': 'Tax Rates',
                'ordering': ['country', 'state', 'tax_class'],
                'unique_together': {('country', 'state', 'tax_class')},
            },
        ),
    ]
