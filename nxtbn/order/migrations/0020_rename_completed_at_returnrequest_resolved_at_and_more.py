# Generated by Django 4.2.11 on 2024-11-04 01:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0019_rename_receving_status_returnlineitem_receiving_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='returnrequest',
            old_name='completed_at',
            new_name='resolved_at',
        ),
        migrations.AddField(
            model_name='returnrequest',
            name='resolved_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='resolved_returns', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='returnrequest',
            name='status',
            field=models.CharField(choices=[('REQUESTED', 'Requested'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected'), ('REVIEWED', 'Reviewed'), ('CANCELLED', 'Cancelled'), ('RESOLVED', 'Resolved')], default='REQUESTED', max_length=20, verbose_name='Return Status'),
        ),
    ]
