# Generated by Django 4.2.11 on 2025-01-05 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0016_suppliertranslation_productvarianttranslation_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='categorytranslation',
            name='meta_description',
            field=models.CharField(blank=True, help_text='Description for search engines.', max_length=350, null=True),
        ),
        migrations.AddField(
            model_name='categorytranslation',
            name='meta_title',
            field=models.CharField(blank=True, help_text='Title for search engine optimization.', max_length=800, null=True),
        ),
        migrations.AddField(
            model_name='collectiontranslation',
            name='meta_description',
            field=models.CharField(blank=True, help_text='Description for search engines.', max_length=350, null=True),
        ),
        migrations.AddField(
            model_name='collectiontranslation',
            name='meta_title',
            field=models.CharField(blank=True, help_text='Title for search engine optimization.', max_length=800, null=True),
        ),
        migrations.AddField(
            model_name='producttagtranslation',
            name='meta_description',
            field=models.CharField(blank=True, help_text='Description for search engines.', max_length=350, null=True),
        ),
        migrations.AddField(
            model_name='producttagtranslation',
            name='meta_title',
            field=models.CharField(blank=True, help_text='Title for search engine optimization.', max_length=800, null=True),
        ),
        migrations.AddField(
            model_name='producttranslation',
            name='meta_description',
            field=models.CharField(blank=True, help_text='Description for search engines.', max_length=350, null=True),
        ),
        migrations.AddField(
            model_name='producttranslation',
            name='meta_title',
            field=models.CharField(blank=True, help_text='Title for search engine optimization.', max_length=800, null=True),
        ),
        migrations.AddField(
            model_name='suppliertranslation',
            name='meta_description',
            field=models.CharField(blank=True, help_text='Description for search engines.', max_length=350, null=True),
        ),
        migrations.AddField(
            model_name='suppliertranslation',
            name='meta_title',
            field=models.CharField(blank=True, help_text='Title for search engine optimization.', max_length=800, null=True),
        ),
        migrations.DeleteModel(
            name='ProductTypeTranslation',
        ),
    ]
