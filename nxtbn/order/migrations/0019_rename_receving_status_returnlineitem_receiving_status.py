# Generated by Django 4.2.11 on 2024-11-03 22:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0018_alter_returnlineitem_receving_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='returnlineitem',
            old_name='receving_status',
            new_name='receiving_status',
        ),
    ]
