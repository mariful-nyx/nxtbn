# Generated by Django 4.2.11 on 2024-10-27 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_alter_order_comment_alter_order_note_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('PROCESSING', 'Processing'), ('SHIPPED', 'Shipped'), ('DELIVERED', 'Delivered'), ('CANCELLED', 'Cancelled'), ('PENDING_RETURN', 'Pending Return'), ('RETURNED', 'Returned')], default='PENDING', help_text='Represents the current stage of the order within its lifecycle.', max_length=20, verbose_name='Order Status'),
        ),
    ]
