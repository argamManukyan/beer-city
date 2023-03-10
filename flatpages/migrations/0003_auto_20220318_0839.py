# Generated by Django 3.1 on 2022-03-18 08:39

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flatpages', '0002_auto_20220318_0837'),
    ]

    operations = [
        migrations.AddField(
            model_name='flatpages',
            name='content_en',
            field=ckeditor_uploader.fields.RichTextUploadingField(null=True),
        ),
        migrations.AddField(
            model_name='flatpages',
            name='content_hy',
            field=ckeditor_uploader.fields.RichTextUploadingField(null=True),
        ),
        migrations.AddField(
            model_name='flatpages',
            name='content_ru',
            field=ckeditor_uploader.fields.RichTextUploadingField(null=True),
        ),
        migrations.AddField(
            model_name='flatpages',
            name='meta_description_en',
            field=models.TextField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='flatpages',
            name='meta_description_hy',
            field=models.TextField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='flatpages',
            name='meta_description_ru',
            field=models.TextField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='flatpages',
            name='meta_title_en',
            field=models.CharField(blank=True, max_length=160, null=True),
        ),
        migrations.AddField(
            model_name='flatpages',
            name='meta_title_hy',
            field=models.CharField(blank=True, max_length=160, null=True),
        ),
        migrations.AddField(
            model_name='flatpages',
            name='meta_title_ru',
            field=models.CharField(blank=True, max_length=160, null=True),
        ),
        migrations.AddField(
            model_name='flatpages',
            name='page_name_en',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='flatpages',
            name='page_name_hy',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='flatpages',
            name='page_name_ru',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
    ]
