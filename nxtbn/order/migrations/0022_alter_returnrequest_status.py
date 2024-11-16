# Generated by Django 4.2.11 on 2024-11-07 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0021_rename_resolved_at_returnrequest_completed_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='returnrequest',
            name='status',
            field=models.CharField(choices=[('REQUESTED', 'Requested'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected'), ('REVIEWED', 'Reviewed'), ('CANCELLED', 'Cancelled'), ('COMPLETED', 'Completed')], default='REQUESTED', max_length=20, verbose_name='Return Status'),
        ),
    ]